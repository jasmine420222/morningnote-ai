# prompt_builder.py
# Purpose: Build a structured, grounded LLM prompt from market data and news.
#
# The prompt includes anti-hallucination instructions to reduce the risk of
# the model making up facts or overstating causality.

import pandas as pd


def build_morningnote_prompt(
    sector: str,
    tickers: list[str],
    market_df: pd.DataFrame,
    news_df: pd.DataFrame
) -> str:
    """
    Build the full LLM prompt for morning note generation.

    Parameters
    ----------
    sector : str
        The selected sector name (e.g., "AI & Semiconductors").
    tickers : list[str]
        The list of tickers being covered.
    market_df : pd.DataFrame
        Market data with columns: ticker, latest_price, previous_close,
        pct_change, volume.
    news_df : pd.DataFrame
        News data with columns: date, ticker, headline, source, url.

    Returns
    -------
    str
        A formatted prompt string ready to send to an LLM API.

    Example
    -------
    >>> prompt = build_morningnote_prompt("Big Tech", ["AAPL", "MSFT"], mkt_df, news_df)
    >>> print(prompt[:200])
    """
    # TODO: Implement this function in Phase 5
    # Hint: Convert market_df and news_df to readable text blocks,
    # then insert them into the prompt template from prompts/morningnote_prompt.txt
    raise NotImplementedError("build_morningnote_prompt() is not yet implemented.")
