# news_loader.py
# Purpose: Fetch real company news headlines using NewsAPI.
#
# IMPORTANT: This module must raise a clear error if the API key is missing
# or if the API call fails. It must NOT generate fake fallback news headlines.
#
# Requires: NEWSAPI_KEY in your .env file
# Sign up at: https://newsapi.org/

import os
from datetime import datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# How many days back to search for news
NEWS_LOOKBACK_DAYS = 3
# Max articles per ticker
MAX_ARTICLES_PER_TICKER = 5


def load_news_for_tickers(
    tickers: list[str],
    lookback_days: int = NEWS_LOOKBACK_DAYS,
) -> pd.DataFrame:
    """
    Fetch real news headlines for a list of tickers using NewsAPI.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols (e.g., ["NVDA", "AMD"]).
    lookback_days : int
        How many calendar days back to search (default: 3).

    Returns
    -------
    pd.DataFrame
        Columns: date, ticker, headline, source, url
        Sorted by date descending.

    Raises
    ------
    ValueError
        If NEWSAPI_KEY is not set in environment variables.
    RuntimeError
        If the NewsAPI request fails (non-200 response).

    Example
    -------
    >>> news_df = load_news_for_tickers(["NVDA", "AMD"])
    >>> print(news_df.head())
    """
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise ValueError(
            "NEWSAPI_KEY is not set. "
            "Add it to your .env file: NEWSAPI_KEY=your_key_here"
        )

    from_date = (datetime.today() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    to_date = datetime.today().strftime("%Y-%m-%d")

    all_rows = []

    for ticker in tickers:
        # Search using the ticker symbol as keyword
        # NewsAPI /v2/everything endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": MAX_ARTICLES_PER_TICKER,
            "apiKey": api_key,
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                f"NewsAPI request failed for ticker '{ticker}'. "
                f"Status: {response.status_code}, "
                f"Message: {response.json().get('message', 'unknown error')}"
            )

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print(f"  [WARNING] No news found for {ticker} in the last {lookback_days} days.")
            continue

        for article in articles:
            all_rows.append({
                "date": article.get("publishedAt", "")[:10],  # Keep only YYYY-MM-DD
                "ticker": ticker,
                "headline": article.get("title", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", ""),
            })

    if not all_rows:
        raise ValueError(
            f"No news articles found for any of the tickers: {tickers}. "
            f"Try increasing lookback_days or check your API key."
        )

    news_df = pd.DataFrame(all_rows, columns=["date", "ticker", "headline", "source", "url"])
    news_df = news_df.sort_values("date", ascending=False).reset_index(drop=True)

    # Drop rows with empty headlines (sometimes NewsAPI returns [Removed] articles)
    news_df = news_df[news_df["headline"].str.strip() != ""]
    news_df = news_df[~news_df["headline"].str.contains(r"\[Removed\]", na=False)]

    return news_df
