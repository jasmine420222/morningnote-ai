# market_data.py
# Purpose: Fetch real stock market data using yfinance.
#
# IMPORTANT: This module must raise a clear error if data cannot be fetched.
# It must NOT silently generate fake fallback prices or volumes.

import yfinance as yf
import pandas as pd


def get_market_data(tickers: list[str]) -> pd.DataFrame:
    """
    Fetch real market data for a list of tickers using yfinance.

    Parameters
    ----------
    tickers : list[str]
        List of stock ticker symbols (e.g., ["NVDA", "AMD"]).

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns:
        ticker, latest_price, previous_close, pct_change, volume

    Raises
    ------
    ValueError
        If market data cannot be fetched for any ticker.

    Example
    -------
    >>> df = get_market_data(["NVDA", "AMD"])
    >>> print(df.columns.tolist())
    ['ticker', 'latest_price', 'previous_close', 'pct_change', 'volume']
    """
    # TODO: Implement this function in Phase 3
    # Hint: Use yf.Ticker(ticker).fast_info or yf.download() to get price data
    raise NotImplementedError("get_market_data() is not yet implemented.")
