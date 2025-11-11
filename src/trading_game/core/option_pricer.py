import numpy as np
from scipy.stats import norm
from typing import Literal, List
from pydantic import BaseModel, Field, field_validator

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

    @field_validator("position")
    def check_positioqn(cls, v):
        if v not in (1, -1):
            raise ValueError("Position must be +1 (long) or -1 (short)")
        return v

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
    option: Option

    def delta(self) -> float:
        d1 = self.option.d1()
        if self.option.option_type == 'call':
            return self.option.position * norm.cdf(d1)
        else:
            return self.option.position * (norm.cdf(d1) - 1)

    def gamma(self) -> float:
        d1 = self.option.d1()
        return self.option.position * norm.pdf(d1) / (self.option.S * self.option.sigma * np.sqrt(self.option.T))

    def vega(self) -> float:
        d1 = self.option.d1()
        return self.option.position * self.option.S * norm.pdf(d1) * np.sqrt(self.option.T) / 100

    def theta(self) -> float:
        d1, d2 = self.option.d1(), self.option.d2()
        first = -(self.option.S * norm.pdf(d1) * self.option.sigma) / (2 * np.sqrt(self.option.T))
        if self.option.option_type == 'call':
            second = -self.option.r * self.option.K * np.exp(-self.option.r * self.option.T) * norm.cdf(d2)
        else:
            second = self.option.r * self.option.K * np.exp(-self.option.r * self.option.T) * norm.cdf(-d2)
        return self.option.position * (first + second) / self.option.base

    def rho(self) -> float:
        d2 = self.option.d2()
        if self.option.option_type == 'call':
            return self.option.position * self.option.K * self.option.T * np.exp(-self.option.r * self.option.T) * norm.cdf(d2) / 100
        else:
            return -self.option.position * self.option.K * self.option.T * np.exp(-self.option.r * self.option.T) * norm.cdf(-d2) / 100

    def all_greeks(self) -> dict:
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho(),
        }
