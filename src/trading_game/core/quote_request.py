import random
from datetime import date, timedelta
from typing import Literal, Optional

from pydantic import BaseModel, model_validator

from trading_game.config.request_pool import get_random_quote_phrase, get_random_response_phrase
from trading_game.config.settings import BASE
from trading_game.core.option_pricer import Strategy
from trading_game.models.street import Investor



class QuoteRequest(BaseModel):
    investor: Investor
    level: Literal['easy', 'hard']
    init_price: float
    strat: Optional[Strategy] = None
    way: Literal['buy', 'sell'] = random.choice(['buy', 'sell'])
    quantity: Optional[float] = random.choice([250_000, 500_000, 1_000_000, 2_000_000])

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
        """
        today = date.today()
        days = int(maturity * BASE)  # Account for leap years
        future_date = today + timedelta(days=days)
        return future_date.strftime("%b%y")

    def generate_request_message(self) -> str:
        strat_data = self.get_strat_data(self.strat)

        name = strat_data["name"].lower()
        maturities = [self.maturity_to_string(mat) for mat in strat_data["maturities"]]
        maturities_str = f"{maturities[0]} " if len(maturities)==1 else f"{'-'.join(maturities)}"
        sorted_strikes = strat_data["strikes"].copy()
        sorted_strikes.sort()
        strikes = [str(k) for k in sorted_strikes]
        strikes_str = f"{strikes[0]} " if len(strikes)==1 else f"{'-'.join(strikes)}"
        qty_str = f"{int(self.quantity / 1_000)}k" if self.quantity < 1_000_000 else f"{int(self.quantity / 1_000_000)}m"

        phrase = get_random_quote_phrase()

        templates = [
            f"{phrase} a {maturities_str} {strikes_str} {name} in {qty_str}",
            f"{phrase} the {maturities_str} {strikes_str} {name}s for {qty_str}",
            f"{phrase} {maturities_str} {strikes_str} {name} {qty_str}"
        ]

        return f"<strong> {self.investor.company} [{self.investor.name}]: </strong> {random.choice(templates)}"

    def evaluate_bid_ask(self, bid: float, ask: float, price: float, vol: float) -> bool:
        mid = self.strat.price(price, vol)
        if self.way=='buy' and ask <= mid + 0.5 * self.investor.width_tolerance * mid:
            return True
        elif self.way=='sell' and bid >= mid - 0.5 * self.investor.width_tolerance * mid :
            return True
        return False

    def generate_response_message(self, accept: bool) -> str:
        if accept:
            return f"<strong> {self.investor.company} [{self.investor.name}]: </strong> {get_random_response_phrase(self.way)}"
        return f"<strong> {self.investor.company} [{self.investor.name}]: </strong> {get_random_response_phrase('pass')}"



