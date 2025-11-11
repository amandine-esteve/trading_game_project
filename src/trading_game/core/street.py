import random
from enum import Enum
from typing import Literal, List, Optional

from pydantic import BaseModel, model_validator

from trading_game.core.option_pricer import Strategy


class TypeInvest(Enum):
    DIR = "Directional"
    VOL = "Volatility"

class StateRequest(Enum):
    INITIALIZED = "Initialized"
    ONGOING = "Ongoing"
    CLOSED = "Closed"

class Investor(BaseModel):
    name: str
    company: str
    type_invest: TypeInvest
    width_tolerance: Optional[float] = None
    client_relationship: Optional[int] = None

    @model_validator(mode="after")
    def set_width_tolerance(self):
        if self.width_tolerance is None:
            self.width_tolerance = random.uniform(0.1,0.6) if self.type_invest == TypeInvest.VOL else random.uniform(0.5, 0.9)
        return self

    @model_validator(mode="after")
    def set_client_relationship(self):
        if self.client_relationship is None:
            self.client_relationship = random.randint(0,10)
        return self

class Street(BaseModel):
    investors: List[Investor]

    @model_validator(mode="after")
    def validate_investors(self):
        if len(self.investors) > 10:
            raise ValueError("Should not be more than 10 investors.")
        return self

class QuoteRequest(BaseModel):
    investor: Investor
    level: Literal['easy', 'hard']
    price: float
    vol: float
    strat: Optional[Strategy] = None

    @model_validator(mode="after")
    def set_strat(self):
        if self.strat is None:
            self.strat = Strategy.generate_random_strategy(self.level, self.price, self.vol)
        return self

    # def generate_message(self) -> str:
    #     message = f"{self.investor.company} [{self.investor.name}]: Hi could I pls get a quote for a "
    #     if len(self.maturities)==1:
    #         message += f"{self.maturities[0]} "
    #     else:
    #         message += f"{' - '.join(str(self.maturities))}"
    #     if len(self.strikes) == 1:
    #         message += f"{self.strikes[0]} "
    #     else :
    #         message += f"{' - '.join(str(self.strikes))} "
    #     message += f"{self.strat}?"
    #     return message





