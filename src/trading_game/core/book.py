from pydantic import BaseModel, Field
from typing import Optional, Dict, Tuple, Union, Literal

from .market import Stock
from .option_pricer import Option, Strategy, Greeks

class Book(BaseModel):

    """
    Portfolio Book for tracking options and stock positions
    Handles trade history, PnL calculation, and risk metrics
    """

    options: Dict[str, Tuple[Option, int]] = Field(default_factory=dict, description="Option positions: {option_id: (Option, quantity)}")
    stock: Optional[Stock] = Field(None, description="Underlying stock")
    stock_quantity: int = Field(0, description="Number of stock shares held")
    trade_history: Dict[str, Tuple[int, float, str, str]] = Field(default_factory=dict, description="Trade history: {trade_id: (quantity, price, asset_type, ref_key)}")
    

    def add_option(self, option: Option, quantity: int, trade_price: float, trade_id: Optional[str] = None) -> str:
        
        """ Add an option position to the book """
        
        # Generate trade_id if not provided
        if trade_id is None:
            trade_id = f"opt_{len(self.trade_history)}"
        
        # Create a unique key for the option
        opt_key = f"{option.option_type}_{option.K}_{option.T:.4f}_{id(option)}"
        
        # Add or update option position
        if opt_key in self.options:
            existing_option, existing_qty = self.options[opt_key]
            new_qty = existing_qty + quantity
            
            # Remove position if quantity becomes zero
            if new_qty == 0:
                del self.options[opt_key]
            else:
                self.options[opt_key] = (option, new_qty)
        else:
            self.options[opt_key] = (option, quantity)
        
        # Record trade in history
        self.trade_history[trade_id] = (quantity, trade_price, "option", opt_key)
        
        return trade_id
    
    def add_strategy(self, strategy: Strategy, quantity: int = 1, trade_prices: Optional[Dict[int, float]] = None) -> list[str]:
        
        """ Add a complete options strategy to the book """

        trade_ids = []
        
        for idx, option in enumerate(strategy.options):
            # Determine trade price
            if trade_prices and idx in trade_prices:
                trade_price = trade_prices[idx]
            else:
                trade_price = option.price()
            
            # Generate trade_id
            trade_id = f"{strategy.name.lower().replace(' ', '_')}_{idx}_{len(self.trade_history)}"
            
            # Add to book
            tid = self.add_option(option, quantity, trade_price, trade_id)
            trade_ids.append(tid)
        
        return trade_ids

    def hedge_with_stock(self, quantity: int, trade_price: Optional[float] = None, trade_id: Optional[str] = None) -> str:
        """ Hedge portfolio by buying/selling stock """
        
        if self.stock is None:
            raise ValueError("Book.stock must be set before hedging.")
        if quantity == 0:
            raise ValueError("quantity must be non-zero.")

        trade_id = trade_id or f"stk_{len(self.trade_history)}"
        self.stock_quantity += quantity
        # (quantity, price, asset_type, ref_key)
        self.trade_history[trade_id] = (quantity, float(trade_price), "stock", "STOCK")
        
        return trade_id
    
    def compute_trade_pnl(self) -> float:
        """ Calculate total PnL from all trades """
        pnl = 0.0
        
        for _ , (quantity, trade_price, asset_type, ref_key) in self.trade_history.items():
            if asset_type == "stock":
                current_price = self.set_last_price()
                pnl += quantity * (current_price - trade_price)
            
            elif asset_type == "option":
                # Find the corresponding option
                if ref_key in self.options:
                    option, _ = self.options[ref_key]
                    current_price = option.price()
                    pnl += quantity * (current_price - trade_price)
        
        return pnl

    def compute_book_value(self) -> float:
        """ Calculate total book value (mark-to-market) """
        value = 0.0
        
        # Value from options
        for opt_key, (option, quantity) in self.options.items():
            value += quantity * option.price()
        
        # Value from stock
        value += self.stock_quantity * self.set_last_price()
        
        return value
    
    def compute_greeks(self) -> Dict[str, float]:
        """ Calculate aggregated Greeks for the entire portfolio """
        
        total_greeks = {
            "delta": 0.0,
            "gamma": 0.0,
            "vega": 0.0,
            "theta": 0.0,
            "rho": 0.0
        }
        
        # Aggregate Greeks from all options
        for opt_key, (option, quantity) in self.options.items():
            greeks_calc = Greeks(option=option)
            option_greeks = greeks_calc.all_greeks()
            
            for greek_name, greek_value in option_greeks.items():
                total_greeks[greek_name] += quantity * greek_value
        
        # Add delta from stock position (1 delta per share)
        total_greeks["delta"] += self.stock_quantity
        
        return total_greeks
    
    def get_positions_summary(self) -> Dict:
        """ Get a summary of all positions in the book """
        
        summary = {
            "options": [],
            "stock": None,
            "total_value": self.compute_book_value(),
            "total_pnl": self.compute_trade_pnl(),
            "greeks": self.compute_greeks()
        }
        
         # Options summary - grouped by strategy characteristics
        for opt_key, (option, quantity) in self.options.items():
            option_greeks = Greeks(option=option).all_greeks()
            
            summary["options"].append({
                "key": opt_key,
                "type": option.option_type.upper(),
                "strike": option.K,
                "maturity": option.T,
                "dte": int(option.T * 365),
                "quantity": abs(quantity),
                "side": "LONG" if quantity > 0 else "SHORT",
                "price": option.price(),
                "value": quantity *option.price(),
                "delta": option_greeks["delta"] * quantity,
                "gamma": option_greeks["gamma"] * quantity,
                "vega": option_greeks["vega"] * quantity,
                "theta": option_greeks["theta"] * quantity
            })
        
        # Stock summary
        summary["stock"] = {
            "ticker": self.stock.ticker,
            "quantity": self.stock_quantity,
            "side": "LONG" if self.stock_quantity > 0 else "SHORT" if self.stock_quantity < 0 else "FLAT",
            "price": self.stock.set_last_price,
            "value": self.stock_quantity * self.stock.set_last_price()
        }
        
        return summary

    # Maybe hide this part, use just if the player doesn't have a clue
    def get_delta_hedge_recommendation(self) -> int:
        """ Calculate recommended stock position to delta-hedge the portfolio """
        current_greeks = self.compute_greeks()
        current_delta = current_greeks["delta"]
        
        # Recommended hedge = negative of current delta
        recommended_shares = -int(round(current_delta))
        
        return recommended_shares
    
    def clear_book(self):
        """Clear all positions and trade history (keeps stock object)"""
        self.options = {}
        self.stock_quantity = 0
        self.trade_history = {}
    
    def remove_option(self, opt_key: str) -> bool:
        """ Remove an option position from the book """
        if opt_key in self.options:
            del self.options[opt_key]
            return True
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
        
    def get_gamma_theta_vega_hedge_recommendation(self) -> dict:
        """
        Return coherent multi-Greek hedge hints based on the joint pattern of
        Gamma, Vega and Theta exposures.
        """

        greeks = self.compute_greeks()
        gamma, vega, theta = greeks["gamma"], greeks["vega"], greeks["theta"]

        profile = ""
        trades = []

        # --- Identify exposure pattern ---
        if gamma > 0 and vega > 0 and theta < 0:
            profile = "long_vol"
            trades.append({
                "action": "SELL",
                "option_type": "CALL or PUT",
                "moneyness": "ATM",
                "maturity": "short-term (1M)",
                "rationale": "Book is long Gamma and Vega but losing Theta → sell short-dated options to monetize time decay."
            })
        elif gamma < 0 and vega < 0 and theta > 0:
            profile = "short_vol"
            trades.append({
                "action": "BUY",
                "option_type": "CALL or PUT",
                "moneyness": "ATM",
                "maturity": "short-term (1M)",
                "rationale": "Book is short Gamma and Vega but gains Theta → buy short-dated options to add convexity and reduce risk of spikes."
            })
        elif gamma > 0 and vega < 0:
            profile = "short_term_long_convex"
            trades.append({
                "action": "BUY",
                "option_type": "CALL or PUT",
                "moneyness": "OTM",
                "maturity": "long-term (6M)",
                "rationale": "Long short-term Gamma but short Vega → buy long-dated OTM options to rebalance Vega exposure."
            })
        elif gamma < 0 and vega > 0:
            profile = "long_term_short_convex"
            trades.append({
                "action": "SELL",
                "option_type": "CALL or PUT",
                "moneyness": "OTM",
                "maturity": "long-term (6M)",
                "rationale": "Short short-term Gamma but long Vega → sell long-dated options to rebalance and recover Theta."
            })
        else:
            profile = "balanced"
            trades.append({
                "action": "HOLD",
                "rationale": "No major misalignment between Gamma, Vega, and Theta."
            })

        return {
            "current_exposure": {"gamma": gamma, "vega": vega, "theta": theta},
            "profile": profile,
            "suggested_trades": trades
        }

    
    