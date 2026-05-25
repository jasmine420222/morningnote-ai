# market_data.py
# Purpose: Fetch real stock market data using yfinance.
#
# IMPORTANT: This module must raise a clear error if data cannot be fetched.
# It must NOT silently generate fake fallback prices or volumes.
#
# No API key required — yfinance is free and open.

import pandas as pd
import yfinance as yf


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
        Columns: ticker, latest_price, previous_close, pct_change, volume
        pct_change is expressed as a percentage (e.g., 1.73 means +1.73%).

    Raises
    ------
    ValueError
        If market data cannot be fetched for any ticker, or if yfinance
        returns empty data (e.g., market is closed and no cached data exists).

    Example
    -------
    >>> df = get_market_data(["NVDA", "AMD"])
    >>> print(df)
       ticker  latest_price  previous_close  pct_change     volume
    0    NVDA        875.40          860.50        1.73   45230000
    1     AMD        142.10          145.20       -2.13   32100000
    """
    rows = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)

            # fast_info is lightweight and doesn't require a full download
            info = stock.fast_info

            latest_price = info.last_price
            previous_close = info.previous_close
            volume = info.last_volume

            # Validate — yfinance sometimes returns None if market is closed
            # or the ticker is invalid
            if latest_price is None or previous_close is None:
                raise ValueError(
                    f"yfinance returned None for '{ticker}'. "
                    f"The market may be closed or the ticker may be invalid."
                )

            pct_change = ((latest_price - previous_close) / previous_close) * 100

            rows.append({
                "ticker": ticker,
                "latest_price": round(latest_price, 2),
                "previous_close": round(previous_close, 2),
                "pct_change": round(pct_change, 2),
                "volume": int(volume) if volume is not None else None,
            })

        except Exception as e:
            raise ValueError(
                f"Failed to fetch market data for '{ticker}': {e}\n"
                f"Check your internet connection or verify the ticker symbol."
            )

    if not rows:
        raise ValueError(f"No market data returned for tickers: {tickers}")

    df = pd.DataFrame(rows, columns=[
        "ticker", "latest_price", "previous_close", "pct_change", "volume"
    ])

    return df


def format_market_data_for_prompt(market_df: pd.DataFrame) -> str:
    """
    Convert market data DataFrame into a readable string for the LLM prompt.

    Parameters
    ----------
    market_df : pd.DataFrame
        Output from get_market_data().

    Returns
    -------
    str
        A formatted string like:
        NVDA: $875.40 (prev close $860.50, +1.73%, vol 45,230,000)
        AMD:  $142.10 (prev close $145.20, -2.13%, vol 32,100,000)
    """
    lines = []
    for _, row in market_df.iterrows():
        sign = "+" if row["pct_change"] >= 0 else ""
        vol_str = f"{int(row['volume']):,}" if row["volume"] is not None else "N/A"
        lines.append(
            f"{row['ticker']}: ${row['latest_price']:.2f} "
            f"(prev close ${row['previous_close']:.2f}, "
            f"{sign}{row['pct_change']:.2f}%, "
            f"vol {vol_str})"
        )
    return "\n".join(lines)


# ── Market Snapshot ──────────────────────────────────────────────────────────

# Major indices, commodities, FX, and bonds available free via yfinance
SNAPSHOT_TICKERS = {
    # Equity indices
    "S&P 500":       "^GSPC",
    "Nasdaq":        "^IXIC",
    "Dow Jones":     "^DJI",
    "Russell 2000":  "^RUT",
    "VIX":           "^VIX",
    # Commodities
    "WTI Oil":       "CL=F",
    "Gold":          "GC=F",
    # Crypto
    "Bitcoin":       "BTC-USD",
    # FX
    "EUR/USD":       "EURUSD=X",
    # Bonds
    "10-Yr Yield":   "^TNX",
}


def get_market_snapshot() -> pd.DataFrame:
    """
    Fetch a broad market snapshot: indices, commodities, FX, and bonds.

    This gives the AI context about the overall market environment,
    not just the selected sector stocks.

    Returns
    -------
    pd.DataFrame
        Columns: name, symbol, latest_price, pct_change

    Example
    -------
    >>> snap = get_market_snapshot()
    >>> print(snap)
    """
    rows = []
    for name, symbol in SNAPSHOT_TICKERS.items():
        try:
            info = yf.Ticker(symbol).fast_info
            latest = info.last_price
            prev   = info.previous_close
            if latest is None or prev is None:
                continue
            pct = round(((latest - prev) / prev) * 100, 2)
            rows.append({
                "name":         name,
                "symbol":       symbol,
                "latest_price": round(latest, 2),
                "pct_change":   pct,
            })
        except Exception:
            # Skip silently — snapshot is best-effort, not mission-critical
            continue

    return pd.DataFrame(rows, columns=["name", "symbol", "latest_price", "pct_change"])


def format_snapshot_for_prompt(snapshot_df: pd.DataFrame) -> str:
    """
    Convert the market snapshot DataFrame into a readable string for the prompt.

    Example output:
        S&P 500  (^GSPC):  5,320.10  (-0.45%)
        Nasdaq   (^IXIC):  16,780.23 (-0.82%)
        VIX      (^VIX):   18.45     (+1.50%)
    """
    if snapshot_df.empty:
        return "Market snapshot unavailable."
    lines = []
    for _, row in snapshot_df.iterrows():
        sign = "+" if row["pct_change"] >= 0 else ""
        lines.append(
            f"{row['name']:<15} ({row['symbol']}): "
            f"{row['latest_price']:>10,.2f}  "
            f"({sign}{row['pct_change']:.2f}%)"
        )
    return "\n".join(lines)


# ── Earnings Calendar ─────────────────────────────────────────────────────────

def get_earnings_calendar(tickers: list[str]) -> pd.DataFrame:
    """
    Fetch the next scheduled earnings date for each ticker using yfinance.

    This tells the AI (and the reader) which companies are reporting soon,
    which is important context for interpreting price movements.

    Returns
    -------
    pd.DataFrame
        Columns: ticker, earnings_date
        'earnings_date' is a string like "2026-05-28" or "Unknown"

    Example
    -------
    >>> cal = get_earnings_calendar(["NVDA", "AMD"])
    >>> print(cal)
    """
    rows = []
    for ticker in tickers:
        try:
            cal = yf.Ticker(ticker).calendar
            # yfinance returns a dict; earnings date is under "Earnings Date"
            if cal is not None and "Earnings Date" in cal:
                date_val = cal["Earnings Date"]
                # date_val can be a list or a single value
                if isinstance(date_val, list) and len(date_val) > 0:
                    date_str = str(date_val[0])[:10]
                else:
                    date_str = str(date_val)[:10]
            else:
                date_str = "Unknown"
        except Exception:
            date_str = "Unknown"

        rows.append({"ticker": ticker, "earnings_date": date_str})

    return pd.DataFrame(rows, columns=["ticker", "earnings_date"])


def format_earnings_for_prompt(earnings_df: pd.DataFrame) -> str:
    """
    Convert the earnings calendar into a readable string for the prompt.

    Example output:
        NVDA: earnings on 2026-05-28
        AMD:  earnings date unknown
    """
    if earnings_df.empty:
        return "Earnings calendar unavailable."
    lines = []
    for _, row in earnings_df.iterrows():
        if row["earnings_date"] == "Unknown":
            lines.append(f"{row['ticker']}: earnings date unknown")
        else:
            lines.append(f"{row['ticker']}: next earnings on {row['earnings_date']}")
    return "\n".join(lines)
