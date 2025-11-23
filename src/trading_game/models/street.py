import random
from typing import List, Optional

from pydantic import BaseModel, model_validator

from trading_game.config.investor_pool import get_random_investors
from trading_game.config.settings import NB_INVESTORS



class Investor(BaseModel):
    name: str
    company: str
    width_tolerance: Optional[float] = None
    client_relationship: Optional[int] = None

    @model_validator(mode="after")
    def set_width_tolerance(self):
        if self.width_tolerance is None:
            self.width_tolerance = random.uniform(0.1,0.2)
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

    @classmethod
    def street(cls):
        investors_data = get_random_investors(NB_INVESTORS, unique_companies=True)
        street_data = [Investor(**investor_data) for investor_data in investors_data]
        return cls(investors=street_data)