import numpy as np
from scipy.stats import norm
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, model_validator

# Vanilla Option Pricer using Black-Scholes Model
class Option(BaseModel):
    S: float = Field(..., gt=0, description="Spot price, must be > 0")
    K: float = Field(..., gt=0, description="Strike price, must be > 0")
    T: float = Field(..., ge=0, description="Maturity in years, must be >= 0")
    r: float = Field(..., description="Risk-free rate")
    sigma: float = Field(..., ge=0, description="Volatility, must be >= 0")
    option_type: Literal['call', 'put']
    base: float = Field(360, description="Base for time calculations, default is 360")
    position: int = Field(1, description="Position: +1 for long, -1 for short") # Default position is long

    @model_validator(mode='after')
    def check_position(self):
        if self.position not in (1, -1):
            raise ValueError("Position must be +1 (long) or -1 (short)")
        return self

    def d1(self) -> float:
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self) -> float:
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_price(self) -> float:
        d1, d2 = self.d1(), self.d2()
        return ((self.S * norm.cdf(d1)) - (self.K * np.exp(-self.r * self.T) * norm.cdf(d2))) * self.position

    def put_price(self) -> float:
        d1, d2 = self.d1(), self.d2()
        return ((self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) - (self.S * norm.cdf(-d1))) * self.position

    def price(self) -> float:
        return self.call_price() if self.option_type == 'call' else self.put_price()

# Strategy Pricer
class Strategy(BaseModel):
    name: str
    options: List[Option]

    def price(self) -> float:
        return sum(option.price() for option in self.options)

    @classmethod
    def call_spread(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):

        k_low, k_high = (K1, K2) if K1 < K2 else (K2, K1)

        opts = [
            Option(S=S, K=k_low, T=T, r=r, sigma=sigma, option_type="call", position=1),    # Long call
            Option(S=S, K=k_high, T=T, r=r, sigma=sigma, option_type="call", position=-1),  # Short call
        ]
        return cls(name="Call Spread", options=opts)

    @classmethod
    def put_spread(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):

        k_low, k_high = (K1, K2) if K1 < K2 else (K2, K1)

        opts = [
            Option(S=S, K=k_high, T=T, r=r, sigma=sigma, option_type="put", position=+1),   # Long put
            Option(S=S, K=k_low,  T=T, r=r, sigma=sigma, option_type="put", position=-1),   # Short put
        ]
        return cls(name="Put Spread", options=opts)

    @classmethod
    def straddle(cls, S: float, K: float, T: float, r: float, sigma: float):
        opts = [
            Option(S=S, K=K, T=T, r=r, sigma=sigma, option_type="call", position=1),    # Long call
            Option(S=S, K=K, T=T, r=r, sigma=sigma, option_type="put", position=1),     # Long put
        ]
        return cls(name="Straddle", options=opts)

    @classmethod
    def strangle(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):
        
        k_low, k_high = (K1, K2) if K1 < K2 else (K2, K1)
        
        opts = [
            Option(S=S, K=k_high, T=T, r=r, sigma=sigma, option_type="call", position=1),    # Long call
            Option(S=S, K=k_low, T=T, r=r, sigma=sigma, option_type="put", position=1),     # Long put with lower strike
        ]
        return cls(name="Strangle", options=opts)

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
    
    def _calculate_single_option_greeks(self, option: Option) -> dict:
        """
        Calculate Greeks for a single option
        Returns raw Greeks (not multiplied by position or quantity)
        """
        if option.T == 0:
            if option.option_type == 'call':
                delta = option.position * (1.0 if option.S > option.K else 0.0)
            else:
                delta = option.position * (-1.0 if option.S < option.K else 0.0)
            
            return {
                "delta": delta,
                "gamma": 0.0,
                "vega": 0.0,
                "theta": 0.0,
                "rho": 0.0
            }
        
        d1 = option.d1()
        d2 = option.d2()
        
        # Delta
        if option.option_type == 'call':
            delta = option.position * norm.cdf(d1)
        else:
            delta = option.position * (norm.cdf(d1) - 1)
        
        # Gamma
        gamma = option.position * norm.pdf(d1) / (option.S * option.sigma * np.sqrt(option.T))
        
        # Vega
        vega = option.position * option.S * norm.pdf(d1) * np.sqrt(option.T) / 100
        
        # Theta
        first_term = -(option.S * norm.pdf(d1) * option.sigma) / (2 * np.sqrt(option.T))
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
    
    def delta(self) -> float:
        """Calculate total Delta"""
        if self._is_strategy():
            # Sum delta across all legs
            return sum(self._calculate_single_option_greeks(opt)["delta"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option)["delta"]
    
    def gamma(self) -> float:
        """Calculate total Gamma"""
        if self._is_strategy():
            # Sum gamma across all legs
            return sum(self._calculate_single_option_greeks(opt)["gamma"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option)["gamma"]
    
    def vega(self) -> float:
        """Calculate total Vega"""
        if self._is_strategy():
            # Sum vega across all legs
            return sum(self._calculate_single_option_greeks(opt)["vega"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option)["vega"]
    
    def theta(self) -> float:
        """Calculate total Theta"""
        if self._is_strategy():
            # Sum theta across all legs
            return sum(self._calculate_single_option_greeks(opt)["theta"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option)["theta"]
    
    def rho(self) -> float:
        """Calculate total Rho"""
        if self._is_strategy():
            # Sum rho across all legs
            return sum(self._calculate_single_option_greeks(opt)["rho"] for opt in self.strategy.options)
        else:
            return self._calculate_single_option_greeks(self.option)["rho"]

    def all_greeks(self) -> dict:
        """ Calculate all Greeks at once """
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho(),
        }
    
    def greeks_by_leg(self) -> List[dict]:
        """ Return Greeks breakdown by leg """
        if self._is_strategy():
            legs = []
            for idx, option in enumerate(self.strategy.options):
                leg_greeks = self._calculate_single_option_greeks(option)
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
            # Single option
            leg_greeks = self._calculate_single_option_greeks(self.option)
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
    
    def summary(self) -> dict:
        """ Get complete summary with total Greeks and per-leg breakdown """
        return {
            "instrument_type": "Strategy" if self._is_strategy() else "Option",
            "name": self.strategy.name if self._is_strategy() else f"{self.option.option_type.upper()} {self.option.K}",
            "total_greeks": self.all_greeks(),
            "legs": self.greeks_by_leg()
        }
