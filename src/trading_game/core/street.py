import random
from datetime import date, timedelta
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
    init_price: float
    strat: Optional[Strategy] = None
    way: Optional[Literal['buy', 'sell']] = random.choice(['buy', 'sell'])

    @model_validator(mode="after")
    def set_strat(self):
        if self.strat is None:
            self.strat = Strategy.generate_random_strategy(self.level, self.init_price)
        return self

    @staticmethod
    def get_strat_data(strat: Strategy) -> dict:
        strat_data = strat.model_dump()
        parsed_data = {"name": strat_data["name"]}
        strikes = list()
        maturities = list()
        for opt in strat_data["options"]:
            strikes.append(opt["K"])
            maturities.append(opt["T"])
        parsed_data["strikes"] = list(set(strikes))
        parsed_data["maturities"] = list(set(maturities))
        return parsed_data

    @staticmethod
    def maturity_to_string(maturity: float) -> str:
        """
        Convert maturity in years to formatted string like 'Jan25', 'Mar26', etc.

        Args:
            maturity: Maturity in years (e.g., 1/12 for 1 month, 1 for 1 year)

        Returns:
            String formatted as first 3 letters of month + 2-digit year
        """
        today = date.today()
        days = int(maturity * 365.25)  # Account for leap years
        future_date = today + timedelta(days=days)

        return future_date.strftime("%b%y")

    def generate_request_message(self) -> str:
        strat_data = self.get_strat_data(self.strat)
        name = strat_data["name"]
        maturities = [self.maturity_to_string(mat) for mat in strat_data["maturities"]]
        strikes = [str(k) for k in strat_data["strikes"]]

        message = f"{self.investor.company} [{self.investor.name}]: Hi could I pls get a quote for a "
        if len(maturities)==1:
            message += f"{maturities[0]} "
        else:
            message += f"{'-'.join(maturities)}"
        if len(strikes) == 1:
            message += f"{strikes[0]} "
        else :
            message += f"{'-'.join(strikes)} "
        message += f"{name.lower()}?"
        return message

    def evaluate_bid_ask(self, bid: float, ask: float, price: float, vol: float) -> bool:
        mid = self.strat.price(price, vol)
        if self.way=='buy' and ask <= mid + 0.5 * self.investor.width_tolerance:
            return True
        elif self.way=='sell' and bid >= mid - 0.5 * self.investor.width_tolerance:
            return True
        return False

    def generate_response_message(self, accept: bool) -> str:
        if self.way=='buy' and accept:
            return "Mine ty"
        elif self.way=='sell' and accept:
            return "Yours ty"
        return "Pass"







