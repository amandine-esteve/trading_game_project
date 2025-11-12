from pydantic import BaseModel
from typing import Optional, Dict, Tuple

from market import Stock
#from ... import Option Ju

class Book(BaseModel):
    options: Optional[Dict[str: int]]=None #change to option (Ju)
    stock_quantity: Optional[int]=0
    trade_history: Optional[Dict[str, Tuple[int, float]]]=None

    def _add_trade(self, asset:Stock|str, trade_price, trade_quantity):
        if asset.__class__.__name__ == 'Option':
            self._options[asset]=trade_quantity
        elif asset.__class__.__name__ == 'Stock':
            self._stock_quantity += trade_quantity
        self._trade_history[asset] = trade_quantity, trade_price

    def _compute_trade_pnl(self):
        pnl = 0
        for asset, trade_q_p in self._trade_history.items():
            pnl += trade_q_p[0] * (asset._price() - trade_q_p[1])
        return pnl

    def _compute_book_value(self):
        value = 0
        delta = 0
        ...
        for option, qty in self._options.items():
            value += qty * option._price()
            delta += qty * option.delta
            ...
        return ...