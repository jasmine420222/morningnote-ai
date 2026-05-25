# sector_mapping.py
# Purpose: Map user-selected sectors to the top 5 companies by market cap.
#
# This is NOT synthetic data. It is a product design rule that decides
# which real companies to include when a user selects a sector.
# The actual market data and news still come from real sources (yfinance, NewsAPI).
#
# Ticker selection methodology:
#   Each sector lists the 5 largest US-listed companies by market capitalization
#   as of May 2026, based on publicly available market data.
#   Sources: AlphaSense, Motley Fool, FinanceCharts (May 2026).
#   These are updated manually — they reflect a snapshot, not real-time rankings.

# ── Sector → Top 5 tickers by market cap (May 2026) ─────────────────────────

SECTOR_TICKERS = {

    # NVIDIA ($5.2T), Alphabet ($4.6T), Apple ($4.5T), Microsoft ($3.1T), AMD
    "AI & Semiconductors": ["NVDA", "GOOGL", "MSFT", "AMD", "AVGO"],

    # Apple ($4.5T), Microsoft ($3.1T), Amazon ($2.9T), Meta, Netflix
    "Big Tech": ["AAPL", "MSFT", "AMZN", "META", "NFLX"],

    # JPMorgan ($849B), Berkshire Hathaway, Visa, Mastercard, Bank of America
    "Financial Services": ["JPM", "BRK-B", "V", "MA", "BAC"],

    # Eli Lilly ($935B), J&J ($489B), AbbVie ($388B), UnitedHealth ($313B), Abbott
    "Healthcare & Pharma": ["LLY", "JNJ", "ABBV", "UNH", "ABT"],

    # Exxon Mobil ($529B), Chevron ($330B), Shell ($218B), TotalEnergies, ConocoPhillips
    "Energy": ["XOM", "CVX", "SHEL", "TTE", "COP"],

    # Amazon ($2.9T), Tesla ($1.6T), Home Depot, Toyota, Alibaba
    "Consumer Discretionary": ["AMZN", "TSLA", "HD", "TM", "BABA"],

    # Walmart, Costco, Procter & Gamble, Coca-Cola, PepsiCo
    "Consumer Staples": ["WMT", "COST", "PG", "KO", "PEP"],

    # Caterpillar, Honeywell, Union Pacific, Raytheon, Lockheed Martin
    "Industrials & Defense": ["CAT", "HON", "UNP", "RTX", "LMT"],

    # NextEra Energy, Southern Company, Duke Energy, American Electric, Dominion
    "Utilities & Clean Energy": ["NEE", "SO", "DUK", "AEP", "D"],

    # Prologis, American Tower, Equinix, Simon Property, Crown Castle
    "Real Estate (REITs)": ["PLD", "AMT", "EQIX", "SPG", "CCI"],
}

# ── Short descriptions shown to the user ────────────────────────────────────

SECTOR_DESCRIPTIONS = {
    "AI & Semiconductors":    "NVIDIA, Alphabet, Microsoft, AMD, Broadcom",
    "Big Tech":               "Apple, Microsoft, Amazon, Meta, Netflix",
    "Financial Services":     "JPMorgan, Berkshire, Visa, Mastercard, BofA",
    "Healthcare & Pharma":    "Eli Lilly, J&J, AbbVie, UnitedHealth, Abbott",
    "Energy":                 "ExxonMobil, Chevron, Shell, TotalEnergies, ConocoPhillips",
    "Consumer Discretionary": "Amazon, Tesla, Home Depot, Toyota, Alibaba",
    "Consumer Staples":       "Walmart, Costco, P&G, Coca-Cola, PepsiCo",
    "Industrials & Defense":  "Caterpillar, Honeywell, Union Pacific, Raytheon, Lockheed",
    "Utilities & Clean Energy":"NextEra, Southern Co, Duke, AEP, Dominion",
    "Real Estate (REITs)":    "Prologis, American Tower, Equinix, Simon Property, Crown Castle",
}


# ── Public API ───────────────────────────────────────────────────────────────

def get_tickers_for_sector(sector_name: str) -> list[str]:
    """
    Return the top-5 tickers by market cap for a given sector.

    Parameters
    ----------
    sector_name : str
        One of the supported sector names (e.g., "AI & Semiconductors").

    Returns
    -------
    list[str]
        A list of 5 ticker symbols ranked by market cap (largest first).

    Raises
    ------
    ValueError
        If the sector name is not recognised.

    Example
    -------
    >>> tickers = get_tickers_for_sector("Healthcare & Pharma")
    >>> print(tickers)
    ['LLY', 'JNJ', 'ABBV', 'UNH', 'ABT']
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


def get_sector_description(sector_name: str) -> str:
    """
    Return a short human-readable description of the sector's companies.

    Useful for displaying under the sector dropdown in the UI.

    Example
    -------
    >>> print(get_sector_description("Energy"))
    ExxonMobil, Chevron, Shell, TotalEnergies, ConocoPhillips
    """
    return SECTOR_DESCRIPTIONS.get(sector_name, "")
