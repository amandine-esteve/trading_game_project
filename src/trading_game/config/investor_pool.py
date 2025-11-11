# Investor pool with realistic names and trading styles

import random

INVESTOR_POOL = [
    # Hedge Funds - Mix of directional and volatility traders
    {"name": "Sarah Chen", "company": "Bridgewater Associates", "type_invest": "Directional"},
    {"name": "Marcus Williams", "company": "Citadel LLC", "type_invest": "Volatility"},
    {"name": "Elena Rodriguez", "company": "Millennium Management", "type_invest": "Directional"},
    {"name": "David Kim", "company": "Two Sigma", "type_invest": "Volatility"},
    {"name": "Alexandra Petrov", "company": "Renaissance Technologies", "type_invest": "Volatility"},
    {"name": "James Patterson", "company": "Elliott Management", "type_invest": "Directional"},
    {"name": "Priya Sharma", "company": "DE Shaw & Co", "type_invest": "Volatility"},
    {"name": "Thomas Anderson", "company": "AQR Capital", "type_invest": "Directional"},

    # Proprietary Trading Firms - Mostly volatility focused
    {"name": "Michael Zhang", "company": "Jane Street Capital", "type_invest": "Volatility"},
    {"name": "Rachel Goldman", "company": "Optiver", "type_invest": "Volatility"},
    {"name": "Kevin O'Brien", "company": "Susquehanna International", "type_invest": "Volatility"},
    {"name": "Yuki Tanaka", "company": "IMC Trading", "type_invest": "Volatility"},
    {"name": "Sofia Martinez", "company": "Flow Traders", "type_invest": "Volatility"},
    {"name": "Daniel Foster", "company": "DRW Trading", "type_invest": "Volatility"},

    # Asset Management - Mostly directional
    {"name": "Catherine Webb", "company": "BlackRock", "type_invest": "Directional"},
    {"name": "Robert Chen", "company": "Vanguard Group", "type_invest": "Directional"},
    {"name": "Jennifer Lee", "company": "Fidelity Investments", "type_invest": "Directional"},
    {"name": "Andrew Morrison", "company": "State Street Global", "type_invest": "Directional"},
    {"name": "Maria Santos", "company": "T. Rowe Price", "type_invest": "Directional"},
    {"name": "William Harris", "company": "Wellington Management", "type_invest": "Directional"},

    # Investment Banks - Mix
    {"name": "Jessica Park", "company": "Goldman Sachs", "type_invest": "Directional"},
    {"name": "Nicholas Brown", "company": "Morgan Stanley", "type_invest": "Volatility"},
    {"name": "Olivia Thompson", "company": "JPMorgan Chase", "type_invest": "Directional"},
    {"name": "Christopher Lee", "company": "Bank of America", "type_invest": "Directional"},
    {"name": "Amanda Singh", "company": "Citigroup", "type_invest": "Volatility"},
    {"name": "Benjamin Taylor", "company": "Barclays Capital", "type_invest": "Volatility"},

    # Family Offices & Private Wealth - Mostly directional
    {"name": "Victoria Rothschild", "company": "Rothschild & Co", "type_invest": "Directional"},
    {"name": "Alexander Hunt", "company": "Soros Fund Management", "type_invest": "Directional"},
    {"name": "Isabella Marino", "company": "Cascade Investment", "type_invest": "Directional"},
    {"name": "Jonathan Clarke", "company": "Tiger Global Management", "type_invest": "Directional"},

    # Boutique Funds - Mix
    {"name": "Emma Wilson", "company": "Pershing Square Capital", "type_invest": "Directional"},
    {"name": "Lucas Mueller", "company": "Third Point LLC", "type_invest": "Directional"},
    {"name": "Sophia Nakamura", "company": "Baupost Group", "type_invest": "Directional"},
    {"name": "Ethan Cooper", "company": "Appaloosa Management", "type_invest": "Directional"},
    {"name": "Chloe Anderson", "company": "Viking Global", "type_invest": "Directional"},
    {"name": "Nathan Brooks", "company": "Point72 Asset Management", "type_invest": "Volatility"},

    # Quant Funds - Volatility focused
    {"name": "Grace Wu", "company": "Medallion Fund", "type_invest": "Volatility"},
    {"name": "Ryan Mitchell", "company": "Quantitative Investment Management", "type_invest": "Volatility"},
    {"name": "Maya Patel", "company": "Winton Capital", "type_invest": "Volatility"},
    {"name": "Oscar Fernandez", "company": "WorldQuant", "type_invest": "Volatility"},

    # Pension & Sovereign Wealth - Directional
    {"name": "Henry Davidson", "company": "CalPERS", "type_invest": "Directional"},
    {"name": "Laura Bennett", "company": "Norway Sovereign Fund", "type_invest": "Directional"},
    {"name": "Charles White", "company": "CPPIB", "type_invest": "Directional"},
    {"name": "Diana Chang", "company": "GIC Private Limited", "type_invest": "Directional"},
]

# Helper functions
import random


def get_random_investor():
    """Returns a random investor from the pool"""
    return random.choice(INVESTOR_POOL)


def get_investors_by_type(type_invest: str):
    """Returns all investors of a specific type ('Directional' or 'Volatility')"""
    return [inv for inv in INVESTOR_POOL if inv["type_invest"] == type_invest]


def get_investors_by_company(company: str):
    """Returns all investors from a specific company"""
    return [inv for inv in INVESTOR_POOL if inv["company"] == company]


def get_random_investors(n: int, unique_companies: bool = False, mixed_types: bool = False):
    """
    Returns n random investors
    If unique_companies=True, ensures no duplicate companies
    If mixed_types=True, ensures at least one DIR and one VOL investor (requires n >= 2)
    """
    if n < 2 and mixed_types:
        raise ValueError("mixed_types requires at least 2 investors (n >= 2)")

    if unique_companies:
        companies_used = set()
        available = INVESTOR_POOL.copy()
        selected = []

        # If mixed_types, ensure we get at least one of each type first
        if mixed_types:
            dir_investors = [inv for inv in available if inv["type_invest"] == "Directional"]
            vol_investors = [inv for inv in available if inv["type_invest"] == "Volatility"]

            # Add one directional
            dir_inv = random.choice(dir_investors)
            selected.append(dir_inv)
            companies_used.add(dir_inv["company"])
            available.remove(dir_inv)

            # Add one volatility (ensuring different company)
            vol_candidates = [inv for inv in vol_investors if inv["company"] not in companies_used]
            if vol_candidates:
                vol_inv = random.choice(vol_candidates)
                selected.append(vol_inv)
                companies_used.add(vol_inv["company"])
                available.remove(vol_inv)

        # Fill remaining slots
        while len(selected) < n and available:
            inv = random.choice(available)
            if inv["company"] not in companies_used:
                selected.append(inv)
                companies_used.add(inv["company"])
            available.remove(inv)

        return selected
    else:
        # Without unique_companies constraint
        if mixed_types:
            dir_investors = [inv for inv in INVESTOR_POOL if inv["type_invest"] == "Directional"]
            vol_investors = [inv for inv in INVESTOR_POOL if inv["type_invest"] == "Volatility"]

            selected = []
            # Add one of each type
            selected.append(random.choice(dir_investors))
            selected.append(random.choice(vol_investors))

            # Fill remaining slots from entire pool
            remaining = n - 2
            if remaining > 0:
                additional = random.sample(INVESTOR_POOL, min(remaining, len(INVESTOR_POOL)))
                selected.extend(additional)

            return selected
        else:
            return random.sample(INVESTOR_POOL, min(n, len(INVESTOR_POOL)))