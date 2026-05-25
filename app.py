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
    page_icon="📈",
    layout="wide",
)

st.title("📈 MorningNote AI")
st.caption("Personalized financial morning briefings powered by AI · Not investment advice")
st.divider()

# ── Sidebar: Watchlist Setup ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Watchlist Setup")

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
    st.caption("📰 News source: NewsAPI → CSV fallback")
    st.caption("📊 Market data: yfinance (free)")

    generate_btn = st.button("🚀 Generate Morning Note", type="primary", use_container_width=True)

# ── Map mode label to build_ticker_list mode key ─────────────────────────────
MODE_MAP = {
    "Sector Watchlist": "sector",
    "Custom Portfolio":  "custom",
    "Sector + Custom":   "mixed",
}

# ── Main area: show content only after button click ───────────────────────────
if not generate_btn:
    st.info("👈 Configure your watchlist in the sidebar, then click **Generate Morning Note**.")
    st.markdown("""
    ### How it works
    1. **Choose a mode** — sector watchlist, your own tickers, or a mix
    2. **Click Generate** — the app fetches real market data and news
    3. **Read two AI-generated notes** — GPT-4o-mini vs Claude Haiku
    4. **Compare** — see which model did better on your watchlist
    """)
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
        st.error(f"❌ {e}")
        st.stop()

st.success(f"**Watchlist:** {note_label}  ·  {', '.join(tickers)}")
st.divider()

# ── Step 2: Fetch all market data ─────────────────────────────────────────────
col_snap, col_stocks = st.columns([1, 1])

with col_snap:
    st.subheader("🌍 Broad Market Snapshot")
    with st.spinner("Fetching indices, commodities, FX..."):
        try:
            snapshot_df = get_market_snapshot()
            st.dataframe(snapshot_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.warning(f"Snapshot unavailable: {e}")
            snapshot_df = None

with col_stocks:
    st.subheader("📊 Your Watchlist Prices")
    with st.spinner("Fetching stock prices from yfinance..."):
        try:
            market_df = get_market_data(tickers)
            # Colour pct_change column: green positive, red negative
            st.dataframe(
                market_df.style.applymap(
                    lambda v: "color: green" if v > 0 else "color: red",
                    subset=["pct_change"],
                ),
                use_container_width=True,
                hide_index=True,
            )
        except Exception as e:
            st.error(f"❌ Failed to fetch stock prices: {e}")
            st.stop()

st.divider()

# ── Step 3: Earnings calendar ─────────────────────────────────────────────────
st.subheader("📅 Earnings Calendar")
with st.spinner("Fetching earnings dates..."):
    try:
        earnings_df = get_earnings_calendar(tickers)
        st.dataframe(earnings_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning(f"Earnings calendar unavailable: {e}")
        earnings_df = None

st.divider()

# ── Step 4: Load news ─────────────────────────────────────────────────────────
st.subheader("📰 Recent News Headlines")
with st.spinner("Loading news (NewsAPI → CSV fallback)..."):
    try:
        news_df = load_news_for_tickers(tickers)
        st.dataframe(
            news_df[["date", "ticker", "headline", "source"]],
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        st.error(f"❌ News loading failed: {e}")
        st.stop()

st.divider()

# ── Step 5: Build prompt ──────────────────────────────────────────────────────
with st.spinner("Assembling prompt..."):
    prompt = build_morningnote_prompt(
        sector      = note_label,
        tickers     = tickers,
        market_df   = market_df,
        news_df     = news_df,
        snapshot_df = snapshot_df,
        earnings_df = earnings_df,
    )

with st.expander("🔍 View prompt sent to both models", expanded=False):
    st.text(prompt)

st.divider()

# ── Step 6: Generate morning notes ───────────────────────────────────────────
st.subheader("🤖 AI-Generated Morning Notes")
st.caption("Both models receive the exact same prompt — the comparison is fair.")

tab_a, tab_b, tab_compare = st.tabs(["Model A — GPT-4o-mini", "Model B — Claude Haiku", "Side-by-Side"])

with st.spinner("Calling both models (this takes ~15 seconds)..."):
    model_a_output, model_b_output = None, None

    # Model A
    try:
        model_a_output = run_openai_model(prompt, model_name="gpt-4o-mini")
        save_note(model_a_output, "outputs/model_a_morning_note.md")
    except Exception as e:
        model_a_output = f"❌ Model A failed: {e}"

    # Model B
    try:
        model_b_output = run_anthropic_model(prompt, model_name="claude-haiku-4-5-20251001")
        save_note(model_b_output, "outputs/model_b_morning_note.md")
    except Exception as e:
        model_b_output = f"❌ Model B failed: {e}"

with tab_a:
    st.markdown(model_a_output)
    st.download_button(
        "⬇️ Download Model A note",
        data=model_a_output,
        file_name="model_a_morning_note.md",
        mime="text/markdown",
    )

with tab_b:
    st.markdown(model_b_output)
    st.download_button(
        "⬇️ Download Model B note",
        data=model_b_output,
        file_name="model_b_morning_note.md",
        mime="text/markdown",
    )

with tab_compare:
    left, right = st.columns(2)
    with left:
        st.markdown("### GPT-4o-mini")
        st.markdown(model_a_output)
    with right:
        st.markdown("### Claude Haiku")
        st.markdown(model_b_output)

st.divider()
st.caption("⚠️ This tool is not investment advice. All AI outputs require human review before acting.")
