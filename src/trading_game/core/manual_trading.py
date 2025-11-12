from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Literal
from enum import Enum
from datetime import datetime
import time

# Imports depuis tes modules existants
# from trading_game.pricer import Option, Strategy
# from trading_game.market import Stock
# from trading_game.book import Book


class OrderSide(Enum):
    BUY = "Buy"
    SELL = "Sell"


class OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"


class OrderStatus(Enum):
    PENDING = "Pending"
    EXECUTED = "Executed"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"


class StrategyType(Enum):
    CALL = "Call"
    PUT = "Put"
    CALL_SPREAD = "CallSpread"
    PUT_SPREAD = "PutSpread"
    STRADDLE = "Straddle"
    STRANGLE = "Strangle"


class Order(BaseModel):
    """Base class for all orders"""
    order_id: Optional[str] = None
    timestamp: Optional[float] = Field(default_factory=time.time)
    side: OrderSide
    order_type: OrderType
    status: OrderStatus = OrderStatus.PENDING
    quantity: int = Field(..., gt=0, description="Quantity must be > 0")
    executed_price: Optional[float] = None
    executed_time: Optional[float] = None
    rejection_reason: Optional[str] = None

    @model_validator(mode='after')
    def set_order_id(self):
        if self.order_id is None:
            self.order_id = f"ORD_{int(self.timestamp * 1000)}"
        return self

    def execute(self, price: float) -> bool:
        """Execute the order at given price"""
        if self.status != OrderStatus.PENDING:
            return False
        
        self.executed_price = price
        self.executed_time = time.time()
        self.status = OrderStatus.EXECUTED
        return True

    def reject(self, reason: str) -> None:
        """Reject the order with a reason"""
        self.status = OrderStatus.REJECTED
        self.rejection_reason = reason

    def cancel(self) -> bool:
        """Cancel a pending order"""
        if self.status != OrderStatus.PENDING:
            return False
        self.status = OrderStatus.CANCELLED
        return True


class VanillaOrder(Order):
    """Order for vanilla options (Call or Put)"""
    option_type: Literal['call', 'put']
    strike: float = Field(..., gt=0, description="Strike must be > 0")
    maturity: float = Field(..., gt=0, description="Maturity in years, must be > 0")
    spot_price: float = Field(..., gt=0, description="Underlying spot price")
    volatility: float = Field(..., gt=0, description="Implied volatility")
    risk_free_rate: float
    limit_price: Optional[float] = None

    @model_validator(mode='after')
    def validate_limit_price(self):
        if self.order_type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError("Limit price must be specified for limit orders")
        return self

    def can_execute(self, market_price: float) -> bool:
        """Check if order can be executed at market price"""
        if self.status != OrderStatus.PENDING:
            return False
        
        if self.order_type == OrderType.MARKET:
            return True
        
        # For limit orders
        if self.side == OrderSide.BUY:
            return market_price <= self.limit_price
        else:  # SELL
            return market_price >= self.limit_price


class StrategyOrder(Order):
    """Order for option strategies (Spread, Straddle, Strangle)"""
    strategy_type: StrategyType
    strikes: List[float] = Field(..., description="List of strikes for the strategy")
    maturity: float = Field(..., gt=0, description="Maturity in years")
    spot_price: float = Field(..., gt=0, description="Underlying spot price")
    volatility: float = Field(..., gt=0, description="Implied volatility")
    risk_free_rate: float
    limit_price: Optional[float] = None
    net_premium: Optional[float] = None

    @model_validator(mode='after')
    def validate_strikes(self):
        """Validate strikes based on strategy type"""
        if self.strategy_type in [StrategyType.CALL_SPREAD, StrategyType.PUT_SPREAD, StrategyType.STRANGLE]:
            if len(self.strikes) != 2:
                raise ValueError(f"{self.strategy_type.value} requires exactly 2 strikes")
            if self.strikes[0] >= self.strikes[1]:
                raise ValueError("First strike must be less than second strike")
        
        elif self.strategy_type == StrategyType.STRADDLE:
            if len(self.strikes) != 1:
                raise ValueError("Straddle requires exactly 1 strike")
        
        return self

    @model_validator(mode='after')
    def validate_limit_price(self):
        if self.order_type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError("Limit price must be specified for limit orders")
        return self

    def can_execute(self, market_price: float) -> bool:
        """Check if strategy order can be executed at market price"""
        if self.status != OrderStatus.PENDING:
            return False
        
        if self.order_type == OrderType.MARKET:
            return True
        
        # For limit orders
        if self.side == OrderSide.BUY:
            return market_price <= self.limit_price
        else:  # SELL
            return market_price >= self.limit_price


class OrderExecutor(BaseModel):
    """Executor that processes and executes orders"""
    pending_orders: List[Order] = Field(default_factory=list)
    executed_orders: List[Order] = Field(default_factory=list)
    rejected_orders: List[Order] = Field(default_factory=list)
    max_position_size: Optional[int] = 1000
    current_position: int = 0

    def submit_order(self, order: Order) -> bool:
        """Submit a new order"""
        # Risk checks
        if not self._check_position_limits(order):
            order.reject("Position limit exceeded")
            self.rejected_orders.append(order)
            return False
        
        self.pending_orders.append(order)
        return True

    def _check_position_limits(self, order: Order) -> bool:
        """Check if order respects position limits"""
        position_change = order.quantity if order.side == OrderSide.BUY else -order.quantity
        new_position = self.current_position + position_change
        
        if abs(new_position) > self.max_position_size:
            return False
        return True

    def execute_vanilla_order(self, order: VanillaOrder, option_class) -> bool:
        """Execute a vanilla option order using the Option class"""
        if order not in self.pending_orders:
            return False
        
        # Create option instance
        opt = option_class(
            K=order.strike,
            T=order.maturity,
            r=order.risk_free_rate,
            option_type=order.option_type,
            position=1 if order.side == OrderSide.BUY else -1
        )
        
        market_price = opt.price(S=order.spot_price, sigma=order.volatility)
        
        # Check if order can execute
        if not order.can_execute(abs(market_price)):
            return False
        
        # Execute order
        success = order.execute(abs(market_price))
        if success:
            self.pending_orders.remove(order)
            self.executed_orders.append(order)
            
            # Update position
            position_change = order.quantity if order.side == OrderSide.BUY else -order.quantity
            self.current_position += position_change
            
        return success

    def execute_strategy_order(self, order: StrategyOrder, strategy_class) -> bool:
        """Execute a strategy order using the Strategy class"""
        if order not in self.pending_orders:
            return False
        
        # Create strategy based on type
        if order.strategy_type == StrategyType.CALL_SPREAD:
            strat = strategy_class.call_spread(
                k1=order.strikes[0],
                k2=order.strikes[1],
                t=order.maturity,
                r=order.risk_free_rate,
            )
        
        elif order.strategy_type == StrategyType.PUT_SPREAD:
            strat = strategy_class.put_spread(
                k1=order.strikes[0],
                k2=order.strikes[1],
                t=order.maturity,
                r=order.risk_free_rate,
            )
        
        elif order.strategy_type == StrategyType.STRADDLE:
            strat = strategy_class.straddle(
                K=order.strikes[0],
                t=order.maturity,
                r=order.risk_free_rate,
            )
        
        elif order.strategy_type == StrategyType.STRANGLE:
            strat = strategy_class.strangle(
                k1=order.strikes[0],
                k2=order.strikes[1],
                t=order.maturity,
                r=order.risk_free_rate,
            )
        
        else:
            order.reject("Unsupported strategy type")
            self.pending_orders.remove(order)
            self.rejected_orders.append(order)
            return False
        
        market_price = abs(strat.price(S=order.spot_price, sigma=order.volatility))
        order.net_premium = market_price
        
        # Check if order can execute
        if not order.can_execute(market_price):
            return False
        
        # Execute order
        success = order.execute(market_price)
        if success:
            self.pending_orders.remove(order)
            self.executed_orders.append(order)
            
            # Update position (strategy counts as 1 position unit per quantity)
            position_change = order.quantity if order.side == OrderSide.BUY else -order.quantity
            self.current_position += position_change
            
        return success

    def cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order by ID"""
        for order in self.pending_orders:
            if order.order_id == order_id:
                if order.cancel():
                    self.pending_orders.remove(order)
                    return True
        return False

    def get_order_status(self, order_id: str) -> Optional[OrderStatus]:
        """Get status of an order by ID"""
        all_orders = self.pending_orders + self.executed_orders + self.rejected_orders
        for order in all_orders:
            if order.order_id == order_id:
                return order.status
        return None

    def get_execution_summary(self) -> dict:
        """Get summary of all executions"""
        return {
            "total_executed": len(self.executed_orders),
            "total_rejected": len(self.rejected_orders),
            "pending": len(self.pending_orders),
            "current_position": self.current_position,
            "total_executed_value": sum(
                o.executed_price * o.quantity 
                for o in self.executed_orders 
                if o.executed_price is not None
            )
        }

#Exemple to show how to use the OrderExecutor with vanilla and strategy orders
# Créer un executor
executor = OrderExecutor(max_position_size=1000)
'''
# Ordre vanilla
vanilla = VanillaOrder(
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    quantity=10,
    option_type='call',
    strike=105,
    maturity=0.25,
    spot_price=100,
    volatility=0.2,
    risk_free_rate=0.05
)

executor.submit_order(vanilla)
executor.execute_vanilla_order(vanilla, option_pricer=pricer)

# Ordre strategy
spread = StrategyOrder(
    side=OrderSide.BUY,
    order_type=OrderType.LIMIT,
    quantity=5,
    strategy_type=StrategyType.CALL_SPREAD,
    strikes=[100, 110],
    maturity=0.5,
    spot_price=105,
    volatility=0.25,
    risk_free_rate=0.05,
    limit_price=3.5
)

executor.submit_order(spread)
executor.execute_strategy_order(spread, strategy_pricer=Strategy)
'''