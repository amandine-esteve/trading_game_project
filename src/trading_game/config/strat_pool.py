import random

import numpy as np
from typing import Literal

from src.trading_game.config.settings import RF

STRATEGY_POOL = {
    'easy':[
        {"name": "call", "strike": 1, "maturity": 1, "call_moneyness": "otm", "option_type": 1},
        {"name": "put", "strike": 1, "maturity": 1, "call_moneyness": "itm", "option_type": 1}
    ],
    'hard':[
        {"name": "call_spread", "strike": 2, "maturity": 1, "call_moneyness": "otm", "option_type": 1},
        {"name": "put_spread", "strike": 2, "maturity": 1, "call_moneyness": "itm", "option_type": 1},
        {"name": "straddle", "strike": 1, "maturity": 1, "call_moneyness": "atm", "option_type": 1},
        {"name": "strangle", "strike": 2, "maturity": 1, "call_moneyness": "atm", "option_type": 1},
        {"name": "calendar_spread", "strike": 1, "maturity": 2, "call_moneyness": "atm", "option_type": 2},
        {"name": "risk_reversal_bullish", "strike": 2, "maturity": 1, "call_moneyness": "otm", "option_type": 1},
        {"name": "risk_reversal_bearish", "strike": 2, "maturity": 1, "call_moneyness": "itm", "option_type": 1},
        {"name": "butterfly", "strike": 3, "maturity": 1, "call_moneyness": "otm", "option_type": 2}
    ]
}

RELATIVE_STRIKE_POOL = np.linspace(0.0, 0.25, 6)
MATURITY_POOL = [1/12, 1/6, 1/4, 1/2, 3/4, 1, 2, 3, 4, 5]

def get_random_strat(level: Literal['easy','hard']) -> dict:
    return random.choice(STRATEGY_POOL[level])

def generate_random_strat_data(level: Literal['easy', 'hard'],  price:float) -> tuple[str, dict]:

    # Choose strategy
    strategy = get_random_strat(level)
    strat = {}

    # Choose strike(s)
    if strategy["strike"] == 1:
        if strategy["call_moneyness"] == "atm":
            factor = 1
        else:
            strike_relative = random.choice(RELATIVE_STRIKE_POOL)
            factor = (1 + strike_relative) if strategy["call_moneyness"] == "otm" else (1 - strike_relative)
        strike = round(factor * price, 0)
        strat["k"] = strike
    elif strategy["call_moneyness"] == "atm":
        strike_relative = random.choice(np.linspace(0.05, 0.15, 4))
        strat["k1"] = round((1 - strike_relative) * price, 0)
        strat["k2"] = round((1 + strike_relative) * price, 0)
    else:
        strikes = list()
        for k in range(1, strategy["strike"]+1):
            strike_relative = random.choice([elem for elem in RELATIVE_STRIKE_POOL if elem not in strikes])
            strikes.append(strike_relative)
            factor = (1 + strike_relative) if strategy["call_moneyness"]=="otm"  else (1 - strike_relative)
            strike = round(factor * price, 0)
            strat[f"k{k}"] = strike

    # Choose maturity
    if strategy["maturity"] == 1:
        strat["t"] = random.choice(MATURITY_POOL)
    else:
        maturities = list()
        for t in range(1, strategy["maturity"]+1):
            maturity = random.choice([elem for elem in MATURITY_POOL if elem not in maturities])
            maturities.append(maturity)
            strat[f"t{t}"] = maturity

    # Choose risk-free rate
    strat["r"] = RF

    # Choose option type if needed
    if strategy["option_type"] > 1:
        strat["option_type"] = random.choice(["call", "put"])

    return strategy["name"], strat




