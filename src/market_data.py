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
