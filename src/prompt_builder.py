# prompt_builder.py
# Purpose: Assemble the final LLM prompt from all available data sources.
#
# Takes raw data (market snapshot, sector stock prices, earnings calendar,
# news headlines) and formats everything into a clean structured text
# ready to send to an AI model.

import pandas as pd

from src.market_data import (
    format_market_data_for_prompt,
    format_snapshot_for_prompt,
    format_earnings_for_prompt,
)

PROMPT_TEMPLATE_PATH = "prompts/morningnote_prompt.txt"


def build_morningnote_prompt(
    sector: str,
    tickers: list[str],
    market_df: pd.DataFrame,
    news_df: pd.DataFrame,
    snapshot_df: pd.DataFrame | None = None,
    earnings_df: pd.DataFrame | None = None,
) -> str:
    """
    Build the full LLM prompt by inserting all data into the prompt template.

    Parameters
    ----------
    sector : str
        Selected sector name (e.g., "AI & Semiconductors").
    tickers : list[str]
        List of tickers being covered.
    market_df : pd.DataFrame
        Sector stock prices from get_market_data().
    news_df : pd.DataFrame
        News headlines from load_news_for_tickers().
    snapshot_df : pd.DataFrame, optional
        Broad market snapshot from get_market_snapshot().
        If None, that section will say "Not available."
    earnings_df : pd.DataFrame, optional
        Earnings calendar from get_earnings_calendar().
        If None, that section will say "Not available."

    Returns
    -------
    str
        Complete prompt string ready to send to an LLM.
    """
    template = _load_template(PROMPT_TEMPLATE_PATH)

    tickers_str   = ", ".join(tickers)
    market_str    = format_market_data_for_prompt(market_df)
    news_str      = _format_news_for_prompt(news_df)
    snapshot_str  = format_snapshot_for_prompt(snapshot_df) if snapshot_df is not None else "Not available."
    earnings_str  = format_earnings_for_prompt(earnings_df) if earnings_df is not None else "Not available."

    prompt = template.format(
        sector        = sector,
        tickers       = tickers_str,
        market_data   = market_str,
        news_data     = news_str,
        snapshot_data = snapshot_str,
        earnings_data = earnings_str,
    )

    return prompt


# ── Private helpers ──────────────────────────────────────────────────────────

def _load_template(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Prompt template not found at '{path}'. "
            f"Make sure prompts/morningnote_prompt.txt exists."
        )


def _format_news_for_prompt(news_df: pd.DataFrame) -> str:
    """
    Convert news DataFrame into readable lines for the prompt.
    If empty, return a note so the model says "evidence is limited."
    """
    if news_df.empty:
        return "No recent news articles found for the selected tickers."
    lines = []
    for _, row in news_df.iterrows():
        lines.append(
            f"[{row['date']}] {row['ticker']} — {row['headline']} ({row['source']})"
        )
    return "\n".join(lines)
