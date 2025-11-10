# Stock pool with realistic volatility ranges by sector
# Volatility values are annualized (typical range: 0.15 to 0.60+)

STOCK_POOL = [
    # Technology - Higher volatility (0.25-0.45)
    {"name": "Apple Inc.", "ticker": "AAPL", "sector": "Technology", "vol": 0.28},
    {"name": "Microsoft Corporation", "ticker": "MSFT", "sector": "Technology", "vol": 0.26},
    {"name": "NVIDIA Corporation", "ticker": "NVDA", "sector": "Technology", "vol": 0.45},
    {"name": "Meta Platforms Inc.", "ticker": "META", "sector": "Technology", "vol": 0.38},
    {"name": "Amazon.com Inc.", "ticker": "AMZN", "sector": "Technology", "vol": 0.32},
    {"name": "Alphabet Inc.", "ticker": "GOOGL", "sector": "Technology", "vol": 0.29},
    {"name": "Oracle Corporation", "ticker": "ORCL", "sector": "Technology", "vol": 0.31},
    {"name": "Salesforce Inc.", "ticker": "CRM", "sector": "Technology", "vol": 0.35},

    # Financial Services - Moderate volatility (0.22-0.35)
    {"name": "JPMorgan Chase & Co.", "ticker": "JPM", "sector": "Financial", "vol": 0.24},
    {"name": "Bank of America Corp.", "ticker": "BAC", "sector": "Financial", "vol": 0.28},
    {"name": "Goldman Sachs Group", "ticker": "GS", "sector": "Financial", "vol": 0.27},
    {"name": "Morgan Stanley", "ticker": "MS", "sector": "Financial", "vol": 0.26},
    {"name": "Visa Inc.", "ticker": "V", "sector": "Financial", "vol": 0.23},
    {"name": "Mastercard Inc.", "ticker": "MA", "sector": "Financial", "vol": 0.24},

    # Healthcare - Moderate volatility (0.20-0.35)
    {"name": "Johnson & Johnson", "ticker": "JNJ", "sector": "Healthcare", "vol": 0.18},
    {"name": "UnitedHealth Group", "ticker": "UNH", "sector": "Healthcare", "vol": 0.22},
    {"name": "Pfizer Inc.", "ticker": "PFE", "sector": "Healthcare", "vol": 0.26},
    {"name": "Moderna Inc.", "ticker": "MRNA", "sector": "Healthcare", "vol": 0.52},
    {"name": "Eli Lilly and Co.", "ticker": "LLY", "sector": "Healthcare", "vol": 0.29},
    {"name": "Merck & Co.", "ticker": "MRK", "sector": "Healthcare", "vol": 0.23},

    # Consumer - Variable volatility (0.20-0.50)
    {"name": "Tesla Inc.", "ticker": "TSLA", "sector": "Automotive", "vol": 0.55},
    {"name": "Nike Inc.", "ticker": "NKE", "sector": "Consumer", "vol": 0.28},
    {"name": "Starbucks Corporation", "ticker": "SBUX", "sector": "Consumer", "vol": 0.27},
    {"name": "McDonald's Corporation", "ticker": "MCD", "sector": "Consumer", "vol": 0.21},
    {"name": "Coca-Cola Company", "ticker": "KO", "sector": "Consumer", "vol": 0.19},
    {"name": "Procter & Gamble Co.", "ticker": "PG", "sector": "Consumer", "vol": 0.17},
    {"name": "Walmart Inc.", "ticker": "WMT", "sector": "Consumer", "vol": 0.22},

    # Energy - Higher volatility (0.30-0.50)
    {"name": "Exxon Mobil Corp.", "ticker": "XOM", "sector": "Energy", "vol": 0.32},
    {"name": "Chevron Corporation", "ticker": "CVX", "sector": "Energy", "vol": 0.31},
    {"name": "ConocoPhillips", "ticker": "COP", "sector": "Energy", "vol": 0.38},
    {"name": "Schlumberger Ltd.", "ticker": "SLB", "sector": "Energy", "vol": 0.42},

    # Utilities - Lower volatility (0.15-0.25)
    {"name": "NextEra Energy Inc.", "ticker": "NEE", "sector": "Utilities", "vol": 0.20},
    {"name": "Duke Energy Corp.", "ticker": "DUK", "sector": "Utilities", "vol": 0.18},
    {"name": "Southern Company", "ticker": "SO", "sector": "Utilities", "vol": 0.17},
    {"name": "Dominion Energy Inc.", "ticker": "D", "sector": "Utilities", "vol": 0.19},

    # Industrial - Moderate volatility (0.23-0.35)
    {"name": "Boeing Company", "ticker": "BA", "sector": "Industrial", "vol": 0.42},
    {"name": "Caterpillar Inc.", "ticker": "CAT", "sector": "Industrial", "vol": 0.29},
    {"name": "General Electric Co.", "ticker": "GE", "sector": "Industrial", "vol": 0.35},
    {"name": "3M Company", "ticker": "MMM", "sector": "Industrial", "vol": 0.26},

    # Telecommunications - Lower-moderate volatility (0.20-0.30)
    {"name": "AT&T Inc.", "ticker": "T", "sector": "Telecom", "vol": 0.24},
    {"name": "Verizon Communications", "ticker": "VZ", "sector": "Telecom", "vol": 0.22},
    {"name": "T-Mobile US Inc.", "ticker": "TMUS", "sector": "Telecom", "vol": 0.28},

    # Entertainment/Media - Higher volatility (0.30-0.45)
    {"name": "Netflix Inc.", "ticker": "NFLX", "sector": "Entertainment", "vol": 0.41},
    {"name": "Walt Disney Company", "ticker": "DIS", "sector": "Entertainment", "vol": 0.31},
    {"name": "Warner Bros Discovery", "ticker": "WBD", "sector": "Entertainment", "vol": 0.48},
]

# Helper function to randomly select a stock
import random


def get_random_stock():
    """Returns a random stock from the pool"""
    return random.choice(STOCK_POOL)


def get_stock_by_ticker(ticker: str):
    """Returns a specific stock by ticker symbol"""
    return next((s for s in STOCK_POOL if s["ticker"] == ticker), None)


def get_stocks_by_sector(sector: str):
    """Returns all stocks from a specific sector"""
    return [s for s in STOCK_POOL if s["sector"] == sector]