from pydantic import BaseModel, model_validator, Field
from enum import Enum
from typing import Optional, List

import random
import numpy as np


class TypeInvest(Enum):
    DIR = "Directional"
    VOL = "Volatility"

class LevelRequest(Enum):
    #FIRST = 1
    EASY = 1
    DIFF = 2

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
    level: LevelRequest
    state: StateRequest
    nb: int
    price: float
    strat: Optional[str] = None
    strikes: Optional[List[float]] = None

    # @model_validator(mode="after")
    # def validate_level(self):
    #     if self.level.value < 3 and self.investor.type_invest == TypeInvest.VOL:
    #         raise ValueError("Investor must be directional for first or easy quote")
    #     if self.level.value == 1 and self.investor.width_tolerance < 0.90:
    #         raise ValueError("Investor must have wide tolerance for first quote")
    #     return self

    @model_validator(mode="after")
    def validate_nb(self):
        if self.nb > 3:
            raise ValueError("Quote cannot be requested again")
        return self

    @model_validator(mode="after")
    def set_strat(self):
        if self.strat is not None:
            return self
        elif self.level.value < 2:
            self.strat = random.choice(["Call", "Put"])  # modify with enum option type (Ju)
        else:
            self.strat = random.choice(["Call", "Put", "CallSpread", "PutSpread", "Straddle", "Strangle"])
        return self

    @model_validator(mode="after")
    def set_strikes(self):
        if self.strikes is not None:
            return self
        elif self.level.value < 2:
            strike_relative = random.choice(np.linspace(0.05, 0.20, 4))
            factor = (1 + strike_relative) if self.strat == "Call" else (1 - strike_relative)
            self.strikes = [int(round(factor * self.price, 0))]
        else:
            ...
        return self

    def _generate_message(self) -> str: # ask chat for diff sentences
        if self.nb == 1:
            message = f"{self.investor.company} [{self.investor.name}]: Hi could I pls get a quote for a "
            if len(self.strikes) == 1:
                message += f"{self.strikes[0]} "
            else :
                message += f"{' - '.join(str(self.strikes))} "
            message += f"{self.strat}?"
            return message
        elif self.nb == 2:
            return f"Ty can I do $xxx more?"
        else:
            return "Great! I'll do $xxx more if ok w u"





