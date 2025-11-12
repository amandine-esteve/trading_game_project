import random

import numpy as np
from typing import Literal

from trading_game.config.settings import RF

STRATEGY_POOL = {
    'easy':[
        {"name": "call", "strike": 1, "maturity": 1, "call_moneyness": "otm"},
        {"name": "put", "strike": 1, "maturity": 1, "call_moneyness": "itm"}
    ],
    'hard':[
        {"name": "call_spread", "strike": 2, "maturity": 1, "call_moneyness": "otm"},
        {"name": "put_spread", "strike": 2, "maturity": 1, "call_moneyness": "itm"},
        {"name": "straddle", "strike": 1, "maturity": 1, "call_moneyness": "atm"},
        {"name": "strangle", "strike": 2, "maturity": 1, "call_moneyness": "atm"},
        {"name": "calendar_spread", "strike": 1, "maturity": 2, "call_moneyness": "atm"},
        {"name": "risk_reversal_bull", "strike": 2, "maturity": 1, "call_moneyness": "otm"},
        {"name": "risk_reversal_bear", "strike": 2, "maturity": 1, "call_moneyness": "itm"},
        {"name": "butterfly_call", "strike": 3, "maturity": 1, "call_moneyness": "atm"},
        {"name": "butterfly_put", "strike": 3, "maturity": 1, "call_moneyness": "atm"}
    ]
}

RELATIVE_STRIKE_POOL = np.linspace(0.0, 0.25, 6)

def get_random_strat(level: Literal['easy','hard']):
    return random.choice(STRATEGY_POOL[level])

def generate_random_strat_data(level: Literal['easy', 'hard'],  price:float, vol: float) -> tuple[str, dict]:

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

    # Choose rest
    strat["t"] = random.choice([1/12, 1/6, 1/4, 1/2, 3/4, 1, 2, 3, 4, 5])
    strat["r"] = RF

    return strategy["name"], strat




