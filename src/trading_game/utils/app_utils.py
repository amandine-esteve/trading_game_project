from trading_game.config.stock_pool import get_random_stock
from trading_game.config.investor_pool import get_random_investors
from trading_game.config.settings import NB_INVESTORS
from trading_game.core.market import Stock
from trading_game.core.street import Investor, Street, QuoteRequest #, LevelRequest, StateRequest


def create_stock():
    stock_data = get_random_stock()
    stock = Stock(**stock_data)
    return stock

def create_street():
    investors_data = get_random_investors(NB_INVESTORS, unique_companies=True, mixed_types=True)
    street_data = [Investor(**investor_data) for investor_data in investors_data]
    street = Street(investors=street_data)
    return street

