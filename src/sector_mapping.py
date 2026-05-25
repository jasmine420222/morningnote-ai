# sector_mapping.py
# Purpose: Map user-selected sectors to a list of stock tickers.
#
# This is NOT synthetic data. It is a product design rule that decides
# which real companies to include when a user selects a sector.
# The actual market data and news still come from real sources.

# Supported sectors and their representative tickers
SECTOR_TICKERS = {
    "AI & Semiconductors": ["NVDA", "AMD", "AVGO", "TSM", "ASML"],
    "Big Tech":            ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
    "Banking":             ["JPM",  "BAC",  "WFC",   "C",    "GS"],
    "Energy":              ["XOM",  "CVX",  "COP",   "SLB",  "EOG"],
}


def get_tickers_for_sector(sector_name: str) -> list[str]:
    """
    Return the list of tickers for a given sector name.

    Parameters
    ----------
    sector_name : str
        One of the supported sector names (e.g., "AI & Semiconductors").

    Returns
    -------
    list[str]
        A list of ticker symbols (e.g., ["NVDA", "AMD", "AVGO", "TSM", "ASML"]).

    Raises
    ------
    ValueError
        If the sector name is not in SECTOR_TICKERS.

    Example
    -------
    >>> tickers = get_tickers_for_sector("Banking")
    >>> print(tickers)
    ['JPM', 'BAC', 'WFC', 'C', 'GS']
    """
    if sector_name not in SECTOR_TICKERS:
        supported = list(SECTOR_TICKERS.keys())
        raise ValueError(
            f"Sector '{sector_name}' is not supported.\n"
            f"Supported sectors: {supported}"
        )
    return SECTOR_TICKERS[sector_name]


def list_available_sectors() -> list[str]:
    """Return all supported sector names."""
    return list(SECTOR_TICKERS.keys())
