from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict

import time
import numpy as np

from settings import RF



class Stock(BaseModel):
    name: str
    ticker: str
    sector: str
    vol: float
    init_price: Optional[float] = 100
    init_time: Optional[float] = Field(default_factory=time.time)
    rate: Optional[float] = RF
    history: Optional[Dict[float, float]] = Field(default_factory=dict)
    last_price: float = None
    last_time: float = None

    @model_validator(mode='after')
    def set_last_price(self):
        self.last_price = self.init_price
        return self

    @model_validator(mode='after')
    def set_last_time(self):
        self.last_time = self.init_time
        return self

    def move_price(self):
        t = time.time()
        delta_t = time.time() - self.last_time
        dt = delta_t/(252*24*3600)

        drift = (self.rate - 0.5 * self.vol ** 2) * dt
        diffusion = self.vol * np.sqrt(dt) * np.random.normal(0, 1)
        p = self.last_price * np.exp(drift + diffusion)

        self.last_price = p
        self.last_time = t
        self.history[t] = p

        return t, p