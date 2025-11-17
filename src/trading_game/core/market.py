from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict

import time
import numpy as np

from trading_game.config.settings import RF
from trading_game.config.stock_pool import get_random_stock



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

    def move_price(self):
        t = time.time()
        delta_t = time.time() - self.last_time
        dt = delta_t/(252*4) #(252*24*3600)

        drift = (self.rate - 0.5 * self.last_vol ** 2) * dt
        diffusion = self.last_vol * np.sqrt(dt) * np.random.normal(0, 1)
        p = self.last_price * np.exp(drift + diffusion)

        self.last_price = p
        self.last_time = t
        self.price_history.append(p)
        self.vol_history.append(self.last_vol)
        self.time_history.append(t)

        return t, p

    def move_vol(self): #implement market shock (also add stock list to keep same length)
        ...
