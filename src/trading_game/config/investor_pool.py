# Investor pool with realistic names and trading styles

import random

INVESTOR_POOL = [
    # Hedge Funds - Mix of directional and volatility traders
    {"name": "Sarah Chen", "company": "Bridgewater Associates"},
    {"name": "Marcus Williams", "company": "Citadel LLC"},
    {"name": "Elena Rodriguez", "company": "Millennium Management"},
    {"name": "David Kim", "company": "Two Sigma"},
    {"name": "Alexandra Petrov", "company": "Renaissance Technologies"},
    {"name": "James Patterson", "company": "Elliott Management"},
    {"name": "Priya Sharma", "company": "DE Shaw & Co"},
    {"name": "Thomas Anderson", "company": "AQR Capital"},

    # Proprietary Trading Firms - Mostly volatility focused
    {"name": "Michael Zhang", "company": "Jane Street Capital"},
    {"name": "Rachel Goldman", "company": "Optiver"},
    {"name": "Kevin O'Brien", "company": "Susquehanna International"},
    {"name": "Yuki Tanaka", "company": "IMC Trading"},
    {"name": "Sofia Martinez", "company": "Flow Traders"},
    {"name": "Daniel Foster", "company": "DRW Trading"},

    # Asset Management - Mostly directional
    {"name": "Catherine Webb", "company": "BlackRock"},
    {"name": "Robert Chen", "company": "Vanguard Group"},
    {"name": "Jennifer Lee", "company": "Fidelity Investments"},
    {"name": "Andrew Morrison", "company": "State Street Global"},
    {"name": "Maria Santos", "company": "T. Rowe Price"},
    {"name": "William Harris", "company": "Wellington Management"},

    # Investment Banks - Mix
    {"name": "Jessica Park", "company": "Goldman Sachs"},
    {"name": "Nicholas Brown", "company": "Morgan Stanley"},
    {"name": "Olivia Thompson", "company": "JPMorgan Chase"},
    {"name": "Christopher Lee", "company": "Bank of America"},
    {"name": "Amanda Singh", "company": "Citigroup"},
    {"name": "Benjamin Taylor", "company": "Barclays Capital"},

    # Family Offices & Private Wealth - Mostly directional
    {"name": "Victoria Rothschild", "company": "Rothschild & Co"},
    {"name": "Alexander Hunt", "company": "Soros Fund Management"},
    {"name": "Isabella Marino", "company": "Cascade Investment"},
    {"name": "Jonathan Clarke", "company": "Tiger Global Management"},

    # Boutique Funds - Mix
    {"name": "Emma Wilson", "company": "Pershing Square Capital"},
    {"name": "Lucas Mueller", "company": "Third Point LLC"},
    {"name": "Sophia Nakamura", "company": "Baupost Group"},
    {"name": "Ethan Cooper", "company": "Appaloosa Management"},
    {"name": "Chloe Anderson", "company": "Viking Global"},
    {"name": "Nathan Brooks", "company": "Point72 Asset Management"},

    # Quant Funds - Volatility focused
    {"name": "Grace Wu", "company": "Medallion Fund"},
    {"name": "Ryan Mitchell", "company": "Quantitative Investment Management"},
    {"name": "Maya Patel", "company": "Winton Capital"},
    {"name": "Oscar Fernandez", "company": "WorldQuant"},

    # Pension & Sovereign Wealth - Directional
    {"name": "Henry Davidson", "company": "CalPERS"},
    {"name": "Laura Bennett", "company": "Norway Sovereign Fund"},
    {"name": "Charles White", "company": "CPPIB"},
    {"name": "Diana Chang", "company": "GIC Private Limited"},
]

# Helper functions
import random


def get_random_investor():
    """Returns a random investor from the pool"""
    return random.choice(INVESTOR_POOL)


def get_investors_by_company(company: str) ->list[dict[str, str]]:
    """Returns all investors from a specific company"""
    return [inv for inv in INVESTOR_POOL if inv["company"] == company]


def get_random_investors(n: int, unique_companies: bool = False) -> list:
    """
    Returns n random investors
    If unique_companies=True, ensures no duplicate companies
    """

    if unique_companies:
        companies_used = set()
        available = INVESTOR_POOL.copy()
        selected = []

        # Fill remaining slots
        while len(selected) < n and available:
            inv = random.choice(available)
            if inv["company"] not in companies_used:
                selected.append(inv)
                companies_used.add(inv["company"])
            available.remove(inv)

        return selected

    else:
        return random.sample(INVESTOR_POOL, min(n, len(INVESTOR_POOL)))