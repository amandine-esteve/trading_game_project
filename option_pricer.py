import numpy as np
from scipy.stats import norm
from typing import Literal, List

# Vanilla Option Pricer using Black-Scholes Model
class Option:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, 
                 option_type: Literal['call', 'put'], position: int = 1):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type
        self.position = position  # +1 pour long, -1 pour short

    def d1(self) -> float:
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self) -> float:
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()
        return ((self.S * norm.cdf(d1)) - (self.K * np.exp(-self.r * self.T) * norm.cdf(d2))) * self.position

    def put_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()
        return ((self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) - (self.S * norm.cdf(-d1))) * self.position

    def price(self) -> float:
        if self.option_type == 'call':
            return self.call_price()
        elif self.option_type == 'put':
            return self.put_price()
        else:
            raise ValueError("option_type must be 'call' or 'put'")

# Strategy Pricer using Black-Scholes Model
class Strategy:
    def __init__(self, name: str, options: List[Option]):
        self.name = name
        self.options = options
    
    def price(self) -> float:
        return sum(option.price() for option in self.options)
    
    @classmethod
    def call_spread(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):
        options = [
            Option(S, K1, T, r, sigma, 'call', position=1),  # Long call
            Option(S, K2, T, r, sigma, 'call', position=-1)   # Short call
        ]
        return cls("Call Spread", options)
    
    @classmethod
    def put_spread(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):
        options = [
            Option(S, K2, T, r, sigma, 'put', position=1),  # Long put
            Option(S, K1, T, r, sigma, 'put', position=-1)   # Short put
        ]
        return cls("Put Spread", options)
    
    @classmethod
    def straddle(cls, S: float, K: float, T: float, r: float, sigma: float):
        options = [
            Option(S, K, T, r, sigma, 'call', position=1),
            Option(S, K, T, r, sigma, 'put', position=1)
        ]
        return cls("Straddle", options)
    
    @classmethod
    def strangle(cls, S: float, K1: float, K2: float, T: float, r: float, sigma: float):
        options = [
            Option(S, K2, T, r, sigma, 'call', position=1),
            Option(S, K1, T, r, sigma, 'put', position=1)
        ]
        return cls("Strangle", options)
    
    def __repr__(self):
        return f"Strategy('{self.name}', {len(self.options)} options, price={self.price():.2f})"

# Example usage:
if __name__ == "__main__":
    # Paramètres du marché
    S = 100      # Spot price
    T = 1.0      # 1 an
    r = 0.05     # Taux 5%
    sigma = 0.2  # Vol 20%
    
    # Option simple
    call = Option(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call')
    print(f"Call simple: {call.price():.2f}")
    
    # Stratégies avec classmethods
    print("\n--- Stratégies ---")
    
    call_spread = Strategy.call_spread(S, K1=95, K2=105, T=T, r=r, sigma=sigma)
    print(call_spread)
    x=call_spread.price()
    print(x)

    put_spread = Strategy.put_spread(S, K1=95, K2=105, T=T, r=r, sigma=sigma)
    print(put_spread)
    
    straddle = Strategy.straddle(S, K=100, T=T, r=r, sigma=sigma)
    print(straddle)
    
    strangle = Strategy.strangle(S, K1=95, K2=105, T=T, r=r, sigma=sigma)
    print(strangle)

