from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal

import time

from trading_game.config.shock_pool import get_random_news_for_sector, format_news



class StateShock(Enum):
    NONE = 0
    HAPPENING = 1
    DECAY = 2

class MarketShock(BaseModel):
    news: str
    shock_type: Literal["positive", "negative"]
    shock_state: StateShock = Field(default=StateShock.NONE)
    shock_time: float = Field(default=0)
    price_impact: float
    vol_spike: float
    vol_decay_rate: float

    class Config:
        use_enum_values = False
        validate_assignment = True

    @classmethod
    def shock(cls, name: str, sector: str):
        random_data = get_random_news_for_sector(sector)
        market_shock_data = format_news(random_data, name)
        return cls(**market_shock_data)

    def trigger_shock(self) -> None:
        self.shock_state = StateShock.HAPPENING
        self.shock_time = time.time()

    def decay_shock(self) -> None:
        self.shock_state = StateShock.DECAY

    def stop_shock(self) -> None:
        self.shock_state = StateShock.NONE
