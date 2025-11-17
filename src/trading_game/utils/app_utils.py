from trading_game.config.investor_pool import get_random_investors
from trading_game.config.settings import NB_INVESTORS
from trading_game.core.street import Investor, Street, QuoteRequest #, LevelRequest, StateRequest

def create_street():
    investors_data = get_random_investors(NB_INVESTORS, unique_companies=True, mixed_types=True)
    street_data = [Investor(**investor_data) for investor_data in investors_data]
    street = Street(investors=street_data)
    return street

