# app.py
# Purpose: A simple Streamlit web app for the MorningNote AI demo.
#
# Run with: streamlit run app.py

import streamlit as st

# Import our own modules from src/
from src.sector_mapping import list_available_sectors, get_tickers_for_sector

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MorningNote AI",
    page_icon="📈",
    layout="centered",
)

st.title("📈 MorningNote AI")
st.caption("An agentic financial briefing generator for equity watchlists.")
st.divider()

# ── Step 1: Sector selection ──────────────────────────────────────────────────
st.subheader("Step 1: Select a Sector")
sector = st.selectbox(
    "Choose an investment sector:",
    options=list_available_sectors(),
)

tickers = get_tickers_for_sector(sector)
st.success(f"Selected tickers: {', '.join(tickers)}")

st.divider()

# ── Step 2: Fetch market data ─────────────────────────────────────────────────
st.subheader("Step 2: Market Data")
st.info("Market data fetching will be implemented in Phase 3.")

# TODO: Replace this placeholder with:
# from src.market_data import get_market_data
# market_df = get_market_data(tickers)
# st.dataframe(market_df)

st.divider()

# ── Step 3: Load news ─────────────────────────────────────────────────────────
st.subheader("Step 3: Company News")
st.info("News loading will be implemented in Phase 4.")

# TODO: Replace this placeholder with:
# from src.news_loader import load_news_for_tickers
# news_df = load_news_for_tickers(tickers)
# st.dataframe(news_df)

st.divider()

# ── Step 4: Generate morning notes ───────────────────────────────────────────
st.subheader("Step 4: Generate Morning Notes")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Model A** — OpenAI gpt-4o-mini")
    st.info("Generation will be implemented in Phase 6.")
with col2:
    st.markdown("**Model B** — Anthropic claude-haiku")
    st.info("Generation will be implemented in Phase 6.")

st.divider()

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption("This tool is not investment advice. All outputs require human review.")
