# prompt_builder.py
# Purpose: Assemble the final LLM prompt from market data and news.
#
# Think of this file as the "briefing preparer":
# it takes raw data (stock prices, news headlines) and formats everything
# into a clean, structured text that can be sent directly to an AI model.
#
# The prompt template lives in: prompts/morningnote_prompt.txt
# This file just fills in the blanks ({sector}, {tickers}, {market_data}, {news_data}).

import pandas as pd

from src.market_data import format_market_data_for_prompt

# Where the prompt template file lives
PROMPT_TEMPLATE_PATH = "prompts/morningnote_prompt.txt"


def build_morningnote_prompt(
    sector: str,
    tickers: list[str],
    market_df: pd.DataFrame,
    news_df: pd.DataFrame,
) -> str:
    """
    Build the full LLM prompt by inserting real data into the prompt template.

    Parameters
    ----------
    sector : str
        The selected sector name (e.g., "AI & Semiconductors").
    tickers : list[str]
        The list of tickers being covered (e.g., ["NVDA", "GOOGL"]).
    market_df : pd.DataFrame
        Output from get_market_data() — columns: ticker, latest_price,
        previous_close, pct_change, volume.
    news_df : pd.DataFrame
        Output from load_news_for_tickers() — columns: date, ticker,
        headline, source, url.

    Returns
    -------
    str
        A complete, ready-to-send prompt string.

    Raises
    ------
    FileNotFoundError
        If the prompt template file is missing.

    Example
    -------
    >>> prompt = build_morningnote_prompt("Big Tech", ["AAPL", "MSFT"], mkt_df, news_df)
    >>> print(prompt[:300])
    """
    # Step 1: Load the prompt template from file
    template = _load_template(PROMPT_TEMPLATE_PATH)

    # Step 2: Format the tickers as a readable comma-separated string
    tickers_str = ", ".join(tickers)

    # Step 3: Format market data into readable lines
    # Uses format_market_data_for_prompt() from market_data.py
    # Example output:
    #   NVDA: $875.40 (prev close $860.50, +1.73%, vol 45,230,000)
    #   AMD:  $142.10 (prev close $145.20, -2.13%, vol 32,100,000)
    market_str = format_market_data_for_prompt(market_df)

    # Step 4: Format news headlines into readable lines
    # Example output:
    #   [2026-05-24] NVDA — Nvidia shares rise as investors focus on AI chip demand (Yahoo Finance)
    news_str = _format_news_for_prompt(news_df)

    # Step 5: Fill in the template placeholders
    prompt = template.format(
        sector=sector,
        tickers=tickers_str,
        market_data=market_str,
        news_data=news_str,
    )

    return prompt


# ── Private helpers ──────────────────────────────────────────────────────────

def _load_template(path: str) -> str:
    """Read the prompt template from disk."""
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
    Convert the news DataFrame into a readable text block for the prompt.

    Each row becomes one line:
    [date] TICKER — headline (source)

    If there are no news rows, return a note saying so — the model
    will then say evidence is limited, which is the correct behaviour.
    """
    if news_df.empty:
        return "No recent news articles found for the selected tickers."

    lines = []
    for _, row in news_df.iterrows():
        lines.append(
            f"[{row['date']}] {row['ticker']} — {row['headline']} ({row['source']})"
        )
    return "\n".join(lines)
