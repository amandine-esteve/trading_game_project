from pathlib import Path
import sys

# Ensure the local 'src' folder is on sys.path so imports resolve when running this script directly.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from trading_game.core.manual_trading import (
    OrderExecutor, VanillaOrder, StrategyOrder,
    OrderSide, OrderType, StrategyType
)
from trading_game.core.option_pricer import Option, Strategy

# Créer un executor
executor = OrderExecutor(max_position_size=1000)

# Test 1: Ordre Call simple
print("=== Test Ordre Call ===")
call_order = VanillaOrder(
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

executor.submit_order(call_order)
print(f"Order ID: {call_order.order_id}")
print(f"Status avant: {call_order.status}")

# Executer l'ordre
success = executor.execute_vanilla_order(call_order, Option)
print(f"✅ Executed: {success}")
print(f"💰 Price: {call_order.executed_price:.4f}")
print(f"Status après: {call_order.status}")


# ===== TEST CALL SPREAD =====
print("=== Test Call Spread ===")

# Créer l'ordre Call Spread
call_spread_order = StrategyOrder(
    side=OrderSide.BUY,              # BUY pour acheter le spread
    order_type=OrderType.MARKET,      # MARKET pour exécution immédiate
    quantity=10,                      # 10 contrats
    strategy_type=StrategyType.CALL_SPREAD,
    strikes=[100, 110],               # Long call à 100, Short call à 110
    maturity=0.5,                     # 6 mois (0.5 ans)
    spot_price=105,                   # Prix du sous-jacent
    volatility=0.25,                  # Vol implicite 25%
    risk_free_rate=0.05               # Taux sans risque 5%
)

# Submit l'ordre
submitted = executor.submit_order(call_spread_order)
print(f"✅ Order submitted: {submitted}")
print(f"📋 Order ID: {call_spread_order.order_id}")
print(f"📊 Status: {call_spread_order.status}")

# Exécuter l'ordre
success = executor.execute_strategy_order(call_spread_order, Strategy)
print(f"\n✅ Executed: {success}")
print(f"💰 Net Premium paid: {call_spread_order.net_premium:.4f}")
print(f"💵 Total cost: {call_spread_order.net_premium * call_spread_order.quantity:.2f}")
print(f"📊 Status: {call_spread_order.status}")
print(f"⏰ Executed at: {call_spread_order.executed_time}")

# Résumé Final (un seul suffit)
print("\n=== Résumé Final ===")
summary = executor.get_execution_summary()
for key, value in summary.items():
    print(f"{key}: {value}")