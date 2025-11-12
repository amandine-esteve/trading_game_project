import numpy as np
from scipy.stats import norm
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, model_validator

from trading_game.config.strat_pool import generate_random_strat_data

# Vanilla Option Pricer using Black-Scholes Model
class Option(BaseModel):
    K: float = Field(..., gt=0, description="Strike price, must be > 0")
    T: float = Field(..., ge=0, description="Maturity in years, must be >= 0")
    r: float = Field(..., description="Risk-free rate")
    option_type: Literal['call', 'put']
    base: float = Field(252, description="Base for time calculations, default is 252")
    position: int = Field(1, description="Position: +1 for long, -1 for short") # Default position is long

    @model_validator(mode='after')
    def check_position(self):
        if self.position not in (1, -1):
            raise ValueError("Position must be +1 (long) or -1 (short)")
        return self

    def d1(self, S: float, sigma: float) -> float:
        return (np.log(S / self.K) + (self.r + 0.5 * sigma ** 2) * self.T) / (sigma * np.sqrt(self.T))

    def d2(self, S: float, sigma: float) -> float:
        return self.d1(S, sigma) - sigma * np.sqrt(self.T)

    def call_price(self, S: float, sigma: float) -> float:
        d1, d2 = self.d1(S, sigma), self.d2(S, sigma)
        return ((S * norm.cdf(d1)) - (self.K * np.exp(-self.r * self.T) * norm.cdf(d2))) * self.position

    def put_price(self, S: float, sigma: float) -> float:
        d1, d2 = self.d1(S, sigma), self.d2(S, sigma)
        return ((self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))) * self.position

    def price(self, S: float, sigma: float) -> float:
        return self.call_price(S, sigma) if self.option_type == 'call' else self.put_price(S, sigma)

# Strategy Pricer
class Strategy(BaseModel):
    name: str
    options: List[Option]

    def price(self, S: float, sigma: float) -> float:
        return sum(option.price(S, sigma) for option in self.options)

    @classmethod
    def call(cls, k: float, t: float, r: float):
        opts = [Option(K=k, T=t, r=r, option_type="call")]
        return cls(name="Call", options=opts)

    @classmethod
    def put(cls, k: float, t: float, r: float):
        opts = [Option(K=k, T=t, r=r, option_type="put")]
        return cls(name="Put", options=opts)

    @classmethod
    def call_spread(cls, k1: float, k2: float, t: float, r: float):
        k_low, k_high = (k1, k2) if k1 < k2 else (k2, k1)

        opts = [
            Option(K=k_low, T=t, r=r, option_type="call", position=1),
            Option(K=k_high, T=t, r=r, option_type="call", position=-1),
        ]
        return cls(name="Call Spread", options=opts)

    @classmethod
    def put_spread(cls, k1: float, k2: float, t: float, r: float):
        k_low, k_high = (k1, k2) if k1 < k2 else (k2, k1)

        opts = [
            Option(K=k_high, T=t, r=r, option_type="put", position=+1),
            Option(K=k_low, T=t, r=r, option_type="put", position=-1),
        ]
        return cls(name="Put Spread", options=opts)

    @classmethod
    def straddle(cls, k: float, t: float, r: float):
        opts = [
            Option(K=k, T=t, r=r, option_type="call", position=1),
            Option(K=k, T=t, r=r, option_type="put", position=1),
        ]
        return cls(name="Straddle", options=opts)

    @classmethod
    def strangle(cls, k1: float, k2: float, t: float, r: float):
        k_low, k_high = (k1, k2) if k1 < k2 else (k2, k1)
        
        opts = [
            Option(K=k_high, T=t, r=r, option_type="call", position=1),
            Option(K=k_low, T=t, r=r, option_type="put", position=1),
        ]
        return cls(name="Strangle", options=opts)

    @classmethod
    def calendar_spread(cls, k: float, t_short: float, t_long: float, r: float, option_type: Literal["call", "put"] = "call"):
        if t_short >= t_long:
            raise ValueError("t_short must be smaller than t_long for a calendar spread")

        opts = [
            Option(K=k, T=t_long, r=r, option_type=option_type, position=+1),
            Option(K=k, T=t_short, r=r, option_type=option_type, position=-1),
        ]
        return cls(name=f"{option_type.capitalize()} Calendar Spread", options=opts)

    @classmethod
    def risk_reversal_bullish(cls, k_put: float, k_call: float, t: float, r: float):
        if k_put >= k_call:
            raise ValueError("For a bullish risk reversal, k_put < k_call is required.")

        opts = [
            Option(K=k_call, T=t, r=r, option_type="call", position=+1),
            Option(K=k_put, T=t, r=r, option_type="put", position=-1),
        ]
        return cls(name="Bull Spread", options=opts)

    @classmethod
    def risk_reversal_bearish(cls, k_put: float, k_call: float, t: float, r: float):
        if k_put >= k_call:
            raise ValueError("For a bearish risk reversal, k_put < k_call is required.")

        opts = [
            Option(K=k_put, T=t, r=r, option_type="put", position=+1), 
            Option(K=k_call, T=t, r=r, option_type="call", position=-1),
        ]
        return cls(name="Bear Spread", options=opts)

    @classmethod
    def butterfly(cls, k1: float, k2: float, k3: float, t: float, r: float, option_type: Literal["call", "put"] = "call"):
        strikes = sorted([k1, k2, k3])
        k_low, k_mid, k_high = strikes

        opts = [
            Option(K=k_low,  T=t, r=r, option_type=option_type, position=+1),
            Option(K=k_mid,  T=t, r=r, option_type=option_type, position=-2),
            Option(K=k_high, T=t, r=r, option_type=option_type, position=+1),
        ]
        return cls(name=f"{option_type.capitalize()} Butterfly", options=opts)

    @staticmethod
    def generate_random_strategy(level: Literal['easy', 'hard'], s: float, sigma: float):
        random_strat_name, random_strat_data = generate_random_strat_data(level, s, sigma)
        generation_method = getattr(Strategy, random_strat_name)
        return generation_method(**random_strat_data)
    
# Greeks Calculator
class Greeks(BaseModel):
    option: Optional[Option] = None
    strategy: Optional[Strategy] = None

    @model_validator(mode='after')
    def ensure_one_is_set(self):
        if (self.option is None) == (self.strategy is None): 
            raise ValueError("Provide exactly one of: option or strategy.")
        return self

    def _is_strategy(self) -> bool:
        return self.strategy is not None

    def _calculate_single_option_greeks(self, option: Option, S: float, sigma: float) -> dict:
        """
        Calculate Greeks for a single option
        Returns raw Greeks (not multiplied by position or quantity)
        """
        if option.T == 0:
            if option.option_type == 'call':
                delta = option.position * (1.0 if S > option.K else 0.0)
            else:
                delta = option.position * (-1.0 if S < option.K else 0.0)
            
            return {
                "delta": delta,
                "gamma": 0.0,
                "vega": 0.0,
                "theta": 0.0,
                "rho": 0.0
            }
        
        d1 = option.d1(S, sigma)
        d2 = option.d2(S, sigma)
        
        # Delta
        if option.option_type == 'call':
            delta = option.position * norm.cdf(d1)
        else:
            delta = option.position * (norm.cdf(d1) - 1)
        
        # Gamma
        gamma = option.position * norm.pdf(d1) / (S * sigma * np.sqrt(option.T))
        
        # Vega
        vega = option.position * S * norm.pdf(d1) * np.sqrt(option.T) / 100
        
        # Theta
        first_term = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(option.T))
        if option.option_type == 'call':
            second_term = -option.r * option.K * np.exp(-option.r * option.T) * norm.cdf(d2)
        else:
            second_term = option.r * option.K * np.exp(-option.r * option.T) * norm.cdf(-d2)
        theta = option.position * (first_term + second_term) / option.base
        
        # Rho
        if option.option_type == 'call':
            rho = option.position * option.K * option.T * np.exp(-option.r * option.T) * norm.cdf(d2) / 100
        else:
            rho = -option.position * option.K * option.T * np.exp(-option.r * option.T) * norm.cdf(-d2) / 100
        
        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho
        }
    
    def delta(self, S: float, sigma: float) -> float:
        """Calculate total Delta"""
        if self._is_strategy():
            return sum(self._calculate_single_option_greeks(opt, S, sigma)["delta"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option, S, sigma)["delta"]
    
    def gamma(self, S: float, sigma: float) -> float:
        """Calculate total Gamma"""
        if self._is_strategy():
            return sum(self._calculate_single_option_greeks(opt, S, sigma)["gamma"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option, S, sigma)["gamma"]
    
    def vega(self, S: float, sigma: float) -> float:
        """Calculate total Vega"""
        if self._is_strategy():
            return sum(self._calculate_single_option_greeks(opt, S, sigma)["vega"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option, S, sigma)["vega"]
    
    def theta(self, S: float, sigma: float) -> float:
        """Calculate total Theta"""
        if self._is_strategy():
            return sum(self._calculate_single_option_greeks(opt, S, sigma)["theta"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option, S, sigma)["theta"]
    
    def rho(self, S: float, sigma: float) -> float:
        """Calculate total Rho"""
        if self._is_strategy():
            return sum(self._calculate_single_option_greeks(opt, S, sigma)["rho"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option, S, sigma)["rho"]

    def all_greeks(self, S: float, sigma: float) -> dict:
        """ Calculate all Greeks at once """
        return {
            "delta": self.delta(S, sigma),
            "gamma": self.gamma(S, sigma),
            "vega": self.vega(S, sigma),
            "theta": self.theta(S, sigma),
            "rho": self.rho(S, sigma),
        }
    
    def greeks_by_leg(self, S: float, sigma: float) -> List[dict]:
        """ Return Greeks breakdown by leg """
        if self._is_strategy():
            legs = []
            for idx, option in enumerate(self.strategy.options):
                leg_greeks = self._calculate_single_option_greeks(option, S, sigma)
                leg_info = {
                    "leg_index": idx,
                    "option_type": option.option_type.upper(),
                    "strike": option.K,
                    "maturity": option.T,
                    "dte": int(option.T * 365),
                    "position": "LONG" if option.position > 0 else "SHORT",
                    "delta": leg_greeks["delta"],
                    "gamma": leg_greeks["gamma"],
                    "vega": leg_greeks["vega"],
                    "theta": leg_greeks["theta"],
                    "rho": leg_greeks["rho"]
                }
                legs.append(leg_info)
            return legs
        else:
            leg_greeks = self._calculate_single_option_greeks(self.option, S, sigma)
            leg_info = {
                "leg_index": 0,
                "option_type": self.option.option_type.upper(),
                "strike": self.option.K,
                "maturity": self.option.T,
                "dte": int(self.option.T * 365),
                "position": "LONG" if self.option.position > 0 else "SHORT",
                "delta": leg_greeks["delta"],
                "gamma": leg_greeks["gamma"],
                "vega": leg_greeks["vega"],
                "theta": leg_greeks["theta"],
                "rho": leg_greeks["rho"]
            }
            return [leg_info]
    
    def summary(self, S: float, sigma: float) -> dict:
        """ Get complete summary with total Greeks and per-leg breakdown """
        return {
            "instrument_type": "Strategy" if self._is_strategy() else "Option",
            "name": self.strategy.name if self._is_strategy() else f"{self.option.option_type.upper()} {self.option.K}",
            "total_greeks": self.all_greeks(S, sigma),
            "legs": self.greeks_by_leg(S, sigma)
        }