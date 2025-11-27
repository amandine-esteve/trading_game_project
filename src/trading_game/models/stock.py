from pydantic import BaseModel, Field, model_validator
from typing import Optional

import time
import numpy as np

from trading_game.config.settings import RF
from trading_game.config.stock_pool import get_random_stock
from trading_game.models.shock import StateShock



class Stock(BaseModel):
    name: str
    ticker: str
    sector: str
    init_price: float
    init_vol: float
    init_time: Optional[float] = Field(default_factory=time.time)
    rate: Optional[float] = RF
    price_history: Optional[list] = None
    vol_history: Optional[list] = None
    time_history: Optional[list] = None
    last_price: float = None
    last_vol: float = None
    last_time: float = None

    @model_validator(mode='after')
    def set_price_history(self):
        self.price_history = [self.init_price]
        return self

    @model_validator(mode='after')
    def set_vol_history(self):
        self.vol_history = [self.init_vol]
        return self

    @model_validator(mode='after')
    def set_time_history(self):
        self.time_history = [self.init_time]
        return self

    @model_validator(mode='after')
    def set_last_price(self):
        self.last_price = self.init_price
        return self

    @model_validator(mode='after')
    def set_last_vol(self):
        self.last_vol = self.init_vol
        return self

    @model_validator(mode='after')
    def set_last_time(self):
        self.last_time = self.init_time
        return self

    @classmethod
    def stock(cls):
        stock_data = get_random_stock()
        return cls(**stock_data)

    def _update_state(self, t: float, p: float, v: float) -> None:
        self.last_time = t
        self.last_price = p
        self.last_vol = v
        self.time_history.append(t)
        self.price_history.append(p)
        self.vol_history.append(v)

    def move_stock(self, shock: dict) -> None:
        t = time.time()
        delta_t = t - self.last_time
        dt = delta_t / (252 * 4)  # (252*24*3600)

        # If shock is triggered apply it to stock
        if shock["shock_state"].value == StateShock.HAPPENING.value:
            print("shock")
            price_change = 1 + shock["price_impact"]
            p = self.last_price * price_change
            v = self.init_vol * shock["vol_spike"]

        # If shock already happened, vol is decaying back to initial level
        else:
            if shock["shock_state"].value == StateShock.DECAY.value:
                time_since_shock = t - shock["shock_time"]
                vol_diff = self.last_vol - self.init_vol
                decay = np.exp(-shock["vol_decay_rate"] * time_since_shock)
                v = self.init_vol + vol_diff * decay
                print("shock decay")

            else:
                v = self.last_vol
                print("no shock")

            drift = (self.rate - 0.5 * v ** 2) * dt
            diffusion = v * np.sqrt(dt) * np.random.normal(0, 1)
            p = self.last_price * np.exp(drift + diffusion)

        self._update_state(t, p, v)


