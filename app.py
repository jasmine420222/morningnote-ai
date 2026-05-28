# app.py
# Purpose: Streamlit interactive demo for MorningNote AI.
# Run with: streamlit run app.py

import os
import sys
import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath('.'))
load_dotenv()

from src.sector_mapping import (
    list_available_sectors,
    get_sector_description,
    build_ticker_list,
)
from src.market_data import (
    get_market_data,
    get_market_snapshot,
    get_earnings_calendar,
    format_snapshot_for_prompt,
    format_earnings_for_prompt,
)
from src.news_loader import load_news_for_tickers
from src.prompt_builder import build_morningnote_prompt
from src.model_runner import run_openai_model, run_anthropic_model, save_note

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MorningNote AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: system-ui, sans-serif;
    background-color: #ffffff;
    color: #111111;
}

.block-container { padding-top: 2rem; max-width: 1200px; }

/* Section headers */
.mn-section {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #444444;
    border-bottom: 1px solid #dddddd;
    padding-bottom: 0.35rem;
    margin: 1.6rem 0 0.8rem;
}

/* News rows */
.mn-news {
    border-left: 3px solid #cccccc;
    padding: 0.45rem 0.8rem;
    margin-bottom: 0.4rem;
    background: #f9f9f9;
    border-radius: 0 5px 5px 0;
}
.mn-news .hl { font-size: 0.9rem; color: #111111; line-height: 1.35; }
.mn-news .meta { font-size: 0.72rem; color: #777777; margin-top: 0.2rem; }
.mn-news .meta b { color: #333333; }

/* AI-generated note: headings slightly larger than body, not giant */
[data-testid="stMarkdownContainer"] h1 { font-size: 1.3rem !important; font-weight: 700; margin: 1rem 0 0.3rem; color: #111; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.2rem !important; font-weight: 700; margin: 0.9rem 0 0.25rem; color: #111; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.1rem !important; font-weight: 700; margin: 0.8rem 0 0.2rem; color: #111; }
[data-testid="stMarkdownContainer"] p  { font-size: 1.0rem; line-height: 1.6; margin: 0.3rem 0; }
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol { font-size: 1.0rem; line-height: 1.6; }

.mn-foot { color: #888888; font-size: 0.75rem; text-align: center; margin-top: 1.5rem; }

/* Page title larger */
h1 { font-size: 2.2rem !important; font-weight: 700 !important; }

/* Metric cards: shrink the big number */
[data-testid="stMetricValue"] { font-size: 1.25rem !important; }
[data-testid="stMetricLabel"] p { font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def section(title: str, sub: str = "") -> None:
    sub_html = f" · <span style='font-weight:400;text-transform:none;letter-spacing:0'>{sub}</span>" if sub else ""
    st.markdown(f"<div class='mn-section'>{title}{sub_html}</div>", unsafe_allow_html=True)


def render_metric_grid(rows: list[tuple[str, str, float]], per_row: int = 5) -> None:
    for start in range(0, len(rows), per_row):
        chunk = rows[start:start + per_row]
        cols = st.columns(per_row)
        for col, (label, value, pct) in zip(cols, chunk):
            with col:
                delta = None if pct is None else f"{pct:+.2f}%"
                st.metric(label=label, value=value, delta=delta)


# ── Header ────────────────────────────────────────────────────────────────────
st.title("MorningNote AI")
st.caption("Personalized AI financial morning briefings — real market data, real headlines, two models compared.")
st.markdown("<div style='font-size:0.75rem;color:#888'>NOT INVESTMENT ADVICE · FOR RESEARCH AND EDUCATION ONLY</div>", unsafe_allow_html=True)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Watchlist Setup")

    mode = st.radio(
        "Choose your mode:",
        options=["Sector Watchlist", "Custom Portfolio", "Sector + Custom"],
        help=(
            "Sector: pick a pre-built industry watchlist\n"
            "Custom: enter your own tickers\n"
            "Sector + Custom: start from a sector, add extra tickers"
        ),
    )

    sector_name  = None
    custom_input = None

    if mode in ("Sector Watchlist", "Sector + Custom"):
        sectors = list_available_sectors()
        sector_name = st.selectbox(
            "Select sector:",
            options=sectors,
            format_func=lambda s: f"{s}  —  {get_sector_description(s)}",
        )

    if mode in ("Custom Portfolio", "Sector + Custom"):
        custom_input = st.text_input(
            "Enter tickers (comma-separated):",
            placeholder="e.g. TSLA, COIN, RBLX, SPOT",
        )

    st.divider()
    st.caption("News: NewsAPI → CSV fallback\nMarket: yfinance (free)\nModels: GPT-4o-mini vs Claude Haiku")
    st.divider()

    generate_btn = st.button("Generate Morning Note", type="primary", use_container_width=True)

# ── Mode map ──────────────────────────────────────────────────────────────────
MODE_MAP = {
    "Sector Watchlist": "sector",
    "Custom Portfolio":  "custom",
    "Sector + Custom":   "mixed",
}

# ── Landing state ─────────────────────────────────────────────────────────────
if not generate_btn:
    st.info("Configure your watchlist in the sidebar, then click Generate Morning Note.")
    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("01", "Choose a mode",   "Sector watchlist, your own tickers, or a mix"),
        ("02", "Generate",        "App pulls live prices, the market snapshot and news"),
        ("03", "Read two notes",  "GPT-4o-mini and Claude Haiku, same prompt"),
        ("04", "Compare",         "Judge which model briefed your watchlist better"),
    ]
    for col, (num, title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(
                f"<div style='border:1px solid #dddddd;border-radius:8px;"
                f"padding:0.9rem 1rem;height:130px'>"
                f"<div style='color:#aaaaaa;font-size:1.3rem;font-weight:600'>{num}</div>"
                f"<div style='font-weight:600;margin:0.3rem 0'>{title}</div>"
                f"<div style='color:#666666;font-size:0.82rem;line-height:1.35'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
    st.stop()

# ── Step 1: Build ticker list ─────────────────────────────────────────────────
with st.spinner("Building watchlist..."):
    try:
        tickers, note_label = build_ticker_list(
            mode         = MODE_MAP[mode],
            sector_name  = sector_name,
            custom_input = custom_input or "",
        )
    except ValueError as e:
        st.error(str(e))
        st.stop()

st.markdown(
    f"<div style='border:1px solid #dddddd;border-left:3px solid #333333;"
    f"border-radius:5px;padding:0.6rem 1rem;background:#f9f9f9'>"
    f"<span style='font-size:0.75rem;font-weight:600;letter-spacing:0.8px;text-transform:uppercase;color:#555'>Watchlist</span>"
    f"&nbsp;&nbsp;<b>{note_label}</b>"
    f"<span style='color:#888'> · {', '.join(tickers)}</span></div>",
    unsafe_allow_html=True,
)

# ── Step 2: Watchlist prices ──────────────────────────────────────────────────
section("Watchlist Prices", "live via yfinance")
with st.spinner("Fetching stock prices..."):
    try:
        market_df = get_market_data(tickers)
        price_rows = [
            (r["ticker"], f"${r['latest_price']:,.2f}", r["pct_change"])
            for _, r in market_df.iterrows()
        ]
        render_metric_grid(price_rows, per_row=5)
    except Exception as e:
        st.error(f"Failed to fetch stock prices: {e}")
        st.stop()

# ── Step 3: Broad market snapshot ─────────────────────────────────────────────
section("Broad Market", "indices · commodities · FX · rates")
with st.spinner("Fetching market snapshot..."):
    try:
        snapshot_df = get_market_snapshot()
        snap_rows = [
            (r["name"], f"{r['latest_price']:,.2f}", r["pct_change"])
            for _, r in snapshot_df.iterrows()
        ]
        render_metric_grid(snap_rows, per_row=5)
    except Exception as e:
        st.warning(f"Snapshot unavailable: {e}")
        snapshot_df = None

# ── Step 4: AI-Generated Morning Notes ───────────────────────────────────────
section("AI-Generated Morning Notes", "both models receive the exact same prompt")

# Load news and earnings silently before building the prompt.
# They will be displayed below in Steps 5 and 6.
with st.spinner("Loading news, earnings and assembling prompt..."):
    try:
        news_df = load_news_for_tickers(tickers)
    except Exception:
        news_df = None

    try:
        earnings_df = get_earnings_calendar(tickers)
    except Exception:
        earnings_df = None

    prompt = build_morningnote_prompt(
        sector      = note_label,
        tickers     = tickers,
        market_df   = market_df,
        news_df     = news_df,
        snapshot_df = snapshot_df,
        earnings_df = earnings_df,
    )

with st.expander("View prompt sent to both models", expanded=False):
    st.text(prompt)

tab_a, tab_b, tab_compare = st.tabs(["Model A · GPT-4o-mini", "Model B · Claude Haiku", "Side-by-Side"])

with st.spinner("Calling both models (this takes ~15 seconds)..."):
    model_a_output, model_b_output = None, None

    try:
        model_a_output = run_openai_model(prompt, model_name="gpt-4o-mini")
        save_note(model_a_output, "outputs/model_a_morning_note.md")
    except Exception as e:
        model_a_output = f"Model A failed: {e}"

    try:
        model_b_output = run_anthropic_model(prompt, model_name="claude-haiku-4-5-20251001")
        save_note(model_b_output, "outputs/model_b_morning_note.md")
    except Exception as e:
        model_b_output = f"Model B failed: {e}"

with tab_a:
    st.markdown(model_a_output)
    st.download_button(
        "Download Model A note",
        data=model_a_output,
        file_name="model_a_morning_note.md",
        mime="text/markdown",
    )

with tab_b:
    st.markdown(model_b_output)
    st.download_button(
        "Download Model B note",
        data=model_b_output,
        file_name="model_b_morning_note.md",
        mime="text/markdown",
    )

with tab_compare:
    left, right = st.columns(2)
    with left:
        st.markdown("<div class='mn-section'>GPT-4o-mini</div>", unsafe_allow_html=True)
        st.markdown(model_a_output)
    with right:
        st.markdown("<div class='mn-section'>Claude Haiku</div>", unsafe_allow_html=True)
        st.markdown(model_b_output)

# ── Step 5: Earnings calendar ─────────────────────────────────────────────────
section("Earnings Calendar", "next scheduled reports")
if earnings_df is not None:
    st.dataframe(earnings_df, use_container_width=True, hide_index=True)
else:
    st.warning("Earnings calendar unavailable.")

# ── Step 6: News headlines ────────────────────────────────────────────────────
section("Recent News Headlines", "last few days")
with st.spinner("Loading news..."):
    try:
        news_df = load_news_for_tickers(tickers)
        for _, r in news_df.head(40).iterrows():
            st.markdown(
                f"<div class='mn-news'>"
                f"<div class='hl'>{r['headline']}</div>"
                f"<div class='meta'><b>{r['ticker']}</b> · {r['source']} · {r['date']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"News loading failed: {e}")

st.markdown(
    "<div class='mn-foot'>This tool is not investment advice. "
    "All AI outputs require human review before acting.</div>",
    unsafe_allow_html=True,
)
