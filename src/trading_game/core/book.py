from pydantic import BaseModel, Field
from typing import Dict, Tuple
from datetime import datetime
import secrets

from trading_game.models.stock import Stock
from .option_pricer import Strategy, Greeks
from trading_game.config.settings import STARTING_CASH

class Book(BaseModel):

    """
    Portfolio Book for tracking options and stock positions
    Handles trade history, PnL calculation, and risk metrics
    """

    trades: Dict[str, Tuple[Strategy, int, float]] = Field(default_factory=dict, description="Trade positions: {ref_key: (Strategy, quantity, entry_price)}")
    stocks: Dict[str, Tuple[Stock, int, float]] = Field(default_factory=dict, description="Trade positions: {ref_key: (Stock, quantity, entry_price)}") # in case we add multiple stocks later
    stock_quantity: int = Field(default=0, description="Number of stock shares held")
    trade_history: Dict[str, Tuple[str, float, int,float, int, float, str, str]] = Field(default_factory=dict, description="Trade history: {trade_id: (time, spot_ref, quantity, price, asset_type, ref_key)}")
    cash: float = Field(default=STARTING_CASH, description="Cash available")

    @staticmethod
    def make_strat_key(strategy: Strategy) -> str:
        """Generate a unique key for the strategy based on its name and a random token."""
        token = secrets.token_hex(4)
        strat_key = f"{strategy.name.replace(' ', '_').lower()}_{token}"
        
        return strat_key

    def is_empty(self) -> bool:
        """Check if the book has no positions."""
        return len(self.trades) == 0 and len(self.stocks) == 0
    
    def is_empty_stock(self) -> bool:
        """ Check if the book has stocks"""
        return len(self.stocks) == 0
    
    def add_trade_strategy(self, strategy: Strategy, quantity: int, spot_ref:float, volatility: float) -> str:
        """Add a strategy trade (not individual legs) to the book"""

        # Generate trade_id for the strategy trade according to time
        timestamp = datetime.now().strftime('%H_%M_%S')
        trade_id = f"strat_{timestamp}"

        # Create a unique key for the strategy (based on its name and legs)
        strat_key = Book.make_strat_key(strategy)

        # If quantity is zero, raise error
        if quantity == 0:
            raise ValueError("Quantity must be non-zero.")
        
        # Extract strikes from strategy for record-keeping
        strikes = [opt.K for opt in strategy.options]

        # Extract maturities from strategy for record-keeping
        maturities = [opt.T for opt in strategy.options]

        # Add the strategy trade to the book
        trade_price= strategy.price(spot_ref, volatility)
        self.trades[strat_key] = (strategy, quantity, trade_price)

        # Record in trade history
        self.trade_history[trade_id] = (
            timestamp,          # time of trade
            spot_ref,           # current spot reference
            quantity,           # quantity bought/sold
            strikes,            # strategy strikes
            maturities,         # strategy maturities
            trade_price,        # transaction price
            strategy,           # asset type
            strat_key           # internal reference key
        )

        # Update the amount of cash available
        self.cash= self.cash - quantity * trade_price

        return trade_id

    def add_trade_stock(self, stock: Stock, quantity: int, spot_ref: float) -> str:
        """Update the quantity of the underlying stock and keep a track record of the trade"""

        # Generate trade_id for the strategy trade according to time
        timestamp = datetime.now().strftime('%H_%M_%S')
        trade_id = f"stock_{timestamp}"

        # Safety check
        if quantity == 0:
            raise ValueError("Quantity must be non-zero.")

        # Update the stock quantity held - Only 1 stock
        self.stock_quantity += quantity

        # Define stock key (unique reference)
        stock_key = f"{stock.ticker}"

        # The 'price' of a stock trade is the spot reference
        trade_price = spot_ref

        # Register trade in the book : update the quantity held
        if stock_key in self.stocks:
            existing_stock, existing_qty, _ = self.stocks[stock_key]
            new_quantity = existing_qty + quantity
            self.stocks[stock_key] = (stock, new_quantity, trade_price)
        else:
            self.stocks[stock_key] = (stock, quantity, trade_price)

        # Record in trade history
        self.trade_history[trade_id] = (
            timestamp,          # time of trade
            spot_ref,           # current spot reference
            quantity,           # quantity bought/sold
            None,
            None,
            trade_price,        # transaction price
            stock.ticker,       # asset type
            stock_key           # internal reference key
        )
        # Update the amount of cash available
        self.cash= self.cash - quantity * trade_price

        return trade_id

    def compute_book_value(self, spot_ref: float, volatility: float) -> float:
        """Calculate total mark-to-market value of the book."""

        value = 0.0

        # ---- Strategies ----
        for strat_key, (strategy, quantity, entry_price) in self.trades.items():
            if isinstance(strategy, Strategy):
                strat_value = strategy.price(spot_ref, volatility)
                value += quantity * strat_value

        # ---- Stocks ----
        for stock_key, (stock, quantity, entry_price) in self.stocks.items():
            stock_value = quantity * spot_ref
            value += stock_value

        # --- Cash ----
        value+=self.cash

        return value

    def stocks_pnl(self, spot_ref: float) -> float:
        total_stock_pnl = 0.0

        for trade_id, record in self.trade_history.items():
            (
                timestamp,      # 0
                spot_trade,     # 1
                quantity,       # 2
                strikes,        # 3
                maturities,     # 4
                trade_price,    # 5
                asset_type,     # 6 (str for a stock, Strategy for options)
                ref_key         # 7 (stock_key ou strat_key)
            ) = record

            # we only keep stocks
            if isinstance(asset_type, str):
                total_stock_pnl+= (spot_ref - trade_price) * quantity

        return total_stock_pnl


    def compute_book_pnl(self, spot_ref: float, volatility: float) -> float:
        """Compute total PnL of the book using trade history."""

        total_pnl = 0.0

        # ---- PnL Strategies ----
        for strat_key, (strategy, quantity, entry_price) in self.trades.items():

            # Mark-to-market PnL
            if isinstance(strategy, Strategy):
                current_price = strategy.price(spot_ref, volatility)

                # Find the last trade price for this strategy from trade history
                matching_trades = [
                    record for record in self.trade_history.values()
                    if record[7] == strat_key and isinstance(record[6], Strategy)
                ]
                if matching_trades:
                    entry_trade_price = matching_trades[-1][5]
                else:
                    entry_trade_price = entry_price  # fallback

                pnl = quantity * (current_price - entry_trade_price)
                total_pnl += pnl

        # ---- PnL Stocks ----
        for stock_key, (stock, quantity, entry_price) in self.stocks.items():
            # Find last stock trade
            matching_trades = [
                record for record in self.trade_history.values()
                if record[7] == stock_key and isinstance(record[6], str)
            ]
            if matching_trades:
                entry_trade_price = matching_trades[-1][5]
            else:
                entry_trade_price = entry_price

            pnl = quantity * (spot_ref - entry_trade_price)
            total_pnl += pnl

        return total_pnl
    
    def strategy_pnl(self, strat_key:float, spot_ref: float, volatility: float) -> float:
        """Compute PnL for a specific strategy in the book."""

        if strat_key not in self.trades:
            raise ValueError(f"Strategy with key {strat_key} not found in the book.")

        strategy, quantity, entry_price = self.trades[strat_key]

        if not isinstance(strategy, Strategy):
            raise ValueError(f"The key {strat_key} does not correspond to a Strategy.")

        current_price = strategy.price(spot_ref, volatility)

        # Find the last trade price for this strategy from trade history
        matching_trades = [
            record for record in self.trade_history.values()
            if record[7] == strat_key and isinstance(record[6], Strategy)
        ]
        if matching_trades:
            entry_trade_price = matching_trades[-1][5]
        else:
            entry_trade_price = entry_price  # fallback

        pnl = quantity * (current_price - entry_trade_price)

        return pnl

    def compute_greeks(self, spot_ref: float, volatility: float) -> Dict[str, float]:
        """Calculate aggregated Greeks for the entire portfolio."""

        # Initialize total Greeks
        total_greeks = {
            "delta": 0.0,
            "gamma": 0.0,
            "vega": 0.0,
            "theta": 0.0,
            "rho": 0.0
        }

        # ---- 1️⃣ From strategies ----
        for strat_key, (strategy, quantity, _) in self.trades.items():
            if isinstance(strategy, Strategy):
                greeks_calc = Greeks(strategy=strategy)
                strat_greeks = greeks_calc.all_greeks(spot_ref, volatility)

                # Aggregate weighted greeks
                for greek_name, greek_value in strat_greeks.items():
                    total_greeks[greek_name] += quantity * greek_value

        # ---- 2️⃣ From stocks ----
        for stock_key, (stock, quantity, _) in self.stocks.items():
            # Each stock has delta = 1 per share
            total_greeks["delta"] += quantity

        return total_greeks

    
    def get_positions_summary(self, spot_ref: float, volatility: float) -> Dict:
        """Get a summary of all positions in the book (strategies + stocks)."""

        # ---- 1️⃣ Global summary ----
        summary = {
            "strategies": [],
            "stocks": [],
            "total_value": self.compute_book_value(spot_ref, volatility),
            "total_pnl": self.compute_book_pnl(spot_ref, volatility),
            "total_greeks": self.compute_greeks(spot_ref, volatility)
        }

        # ---- 2️⃣ Strategies summary ----
        for strat_key, (strategy, quantity, entry_price) in self.trades.items():
            if isinstance(strategy, Strategy):

                # Greeks + current value
                strat_greeks = Greeks(strategy=strategy).all_greeks(spot_ref, volatility)
                current_value = strategy.price(spot_ref, volatility)
                strat_side = "LONG" if quantity > 0 else "SHORT"

                summary["strategies"].append({
                    "key": strat_key,
                    "name": strategy.name,
                    "quantity": abs(quantity),
                    "side": strat_side,
                    "entry_price": entry_price,
                    "current_price": current_value,
                    "value": quantity * current_value,
                    "delta": strat_greeks["delta"] * quantity,
                    "gamma": strat_greeks["gamma"] * quantity,
                    "vega": strat_greeks["vega"] * quantity,
                    "theta": strat_greeks["theta"] * quantity,
                    "rho": strat_greeks["rho"] * quantity
                })

        # ---- 3️⃣ Stocks summary ----
        for stock_key, (stock, quantity, entry_price) in self.stocks.items():
            stock_side = (
                "LONG" if quantity > 0 else
                "SHORT" if quantity < 0 else
                "FLAT"
            )
            stock_value = quantity * spot_ref

            summary["stocks"].append({
                "ticker": stock.ticker,
                "quantity": abs(quantity),
                "side": stock_side,
                "entry_price": entry_price,
                "current_price": spot_ref,
                "value": stock_value,
                "delta": quantity,  # 1 delta per share
                "gamma": 0.0,
                "vega": 0.0,
                "theta": 0.0,
                "rho": 0.0
            })

        return summary
    
    # If the player wants to reset their book
    def clear_book(self):
        """Clear all positions and trade history (keeps stock objects structure)."""
        
        # Remove all strategy and stock positions
        self.trades.clear()
        self.stocks.clear()

        # Reset aggregate stock quantity
        self.stock_quantity = 0

        # Clear trade history
        self.trade_history.clear()

    
    def remove_position(self, position_key: str) -> bool:
        """Remove a strategy or stock position from the book by its key."""

        # Try removing a strategy position
        if position_key in self.trades:
            del self.trades[position_key]
            return True

        # Try removing a stock position
        if position_key in self.stocks:
            del self.stocks[position_key]
            return True

        # Nothing found
        return False
    
    @staticmethod
    def _exposure_level(x: float, low: float, high: float) -> str:
        """ Check if the exposure is in the limits range"""
        if abs(x) < low:
            return "neutral"
        elif abs(x) < high:
            return "moderate"
        else:
            return "high"


