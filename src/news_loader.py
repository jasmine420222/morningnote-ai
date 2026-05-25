# news_loader.py
# Purpose: Fetch real company news headlines using NewsAPI.
#          If the API fails (no key, quota exceeded, network error),
#          automatically falls back to data/sample_news.csv.
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
# Path to the local CSV backup
CSV_BACKUP_PATH = "data/sample_news.csv"


def load_news_for_tickers(
    tickers: list[str],
    lookback_days: int = NEWS_LOOKBACK_DAYS,
    csv_path: str = CSV_BACKUP_PATH,
) -> pd.DataFrame:
    """
    Fetch real news headlines for a list of tickers.

    Strategy:
    1. Try NewsAPI first (live, real-time news).
    2. On success, save results to csv_path so the CSV stays up to date.
    3. If NewsAPI fails for any reason, fall back to the saved CSV.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols (e.g., ["NVDA", "AMD"]).
    lookback_days : int
        How many calendar days back to search (default: 3).
    csv_path : str
        Path to the CSV backup file (default: data/sample_news.csv).

    Returns
    -------
    pd.DataFrame
        Columns: date, ticker, headline, source, url
        Sorted by date descending.

    Raises
    ------
    RuntimeError
        Only if BOTH NewsAPI AND the CSV fallback fail.
    """
    # ── Try NewsAPI first ────────────────────────────────────────────────────
    api_error_msg = None  # store error message before the except block clears it
    try:
        news_df = _fetch_from_newsapi(tickers, lookback_days)

        # Save to CSV so the backup stays fresh
        news_df.to_csv(csv_path, index=False)
        print(f"[news_loader] Fetched {len(news_df)} articles from NewsAPI. Saved to {csv_path}.")
        return news_df

    except Exception as api_error:
        api_error_msg = str(api_error)
        print(f"[news_loader] NewsAPI failed: {api_error_msg}")
        print(f"[news_loader] Falling back to saved CSV: {csv_path}")

    # ── Fallback: load from CSV ──────────────────────────────────────────────
    try:
        return _load_from_csv(tickers, csv_path)
    except Exception as csv_error:
        raise RuntimeError(
            f"Both NewsAPI and CSV fallback failed.\n"
            f"  NewsAPI error: {api_error_msg}\n"
            f"  CSV error: {csv_error}\n"
            f"Fix: run the notebook once with a valid NEWSAPI_KEY to populate {csv_path}."
        )


# ── Private helpers ──────────────────────────────────────────────────────────

def _fetch_from_newsapi(tickers: list[str], lookback_days: int) -> pd.DataFrame:
    """Call NewsAPI and return a DataFrame. Raises on any failure."""
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise ValueError(
            "NEWSAPI_KEY is not set. Add it to your .env file: NEWSAPI_KEY=your_key_here"
        )

    from_date = (datetime.today() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    to_date = datetime.today().strftime("%Y-%m-%d")

    all_rows = []

    for ticker in tickers:
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

        articles = response.json().get("articles", [])
        if not articles:
            print(f"  [WARNING] No news found for {ticker} in the last {lookback_days} days.")
            continue

        for article in articles:
            all_rows.append({
                "date": article.get("publishedAt", "")[:10],
                "ticker": ticker,
                "headline": article.get("title", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", ""),
            })

    if not all_rows:
        raise ValueError(f"No news articles found for any of the tickers: {tickers}.")

    news_df = pd.DataFrame(all_rows, columns=["date", "ticker", "headline", "source", "url"])
    news_df = news_df.sort_values("date", ascending=False).reset_index(drop=True)

    # Drop removed/empty articles (NewsAPI sometimes returns [Removed] placeholders)
    news_df = news_df[news_df["headline"].str.strip() != ""]
    news_df = news_df[~news_df["headline"].str.contains(r"\[Removed\]", na=False)]

    return news_df


def _load_from_csv(tickers: list[str], csv_path: str) -> pd.DataFrame:
    """Load news from local CSV and filter by ticker list. Raises if file missing or empty."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    required_cols = {"date", "ticker", "headline", "source", "url"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV is missing required columns. Expected: {required_cols}")

    filtered = df[df["ticker"].isin(tickers)].copy()

    if filtered.empty:
        raise ValueError(
            f"CSV exists but contains no rows for tickers: {tickers}. "
            f"Run once with a valid NEWSAPI_KEY to populate the CSV."
        )

    return filtered.sort_values("date", ascending=False).reset_index(drop=True)
