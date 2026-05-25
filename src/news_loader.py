# news_loader.py
# Purpose: Load real company news headlines from a saved CSV file.
#
# IMPORTANT: This module must raise a clear error if the CSV file is missing.
# It must NOT generate fake fallback news headlines.

import pandas as pd


def load_news_for_tickers(
    tickers: list[str],
    csv_path: str = "data/sample_news.csv"
) -> pd.DataFrame:
    """
    Load real news headlines for selected tickers from a CSV file.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols to filter news for.
    csv_path : str
        Path to the CSV file containing news data.
        Expected columns: date, ticker, headline, source, url

    Returns
    -------
    pd.DataFrame
        Rows from the CSV where the 'ticker' column matches one of the
        requested tickers.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at csv_path.
    ValueError
        If the CSV file is missing required columns.

    Example
    -------
    >>> news_df = load_news_for_tickers(["NVDA", "AMD"])
    >>> print(news_df.head())
    """
    # TODO: Implement this function in Phase 4
    # Hint: Use pd.read_csv(csv_path) then filter by ticker column
    raise NotImplementedError("load_news_for_tickers() is not yet implemented.")
