import random
from datetime import datetime, timedelta

import pandas as pd

from trading_game.config.settings import RF
from trading_game.core.quote_request import QuoteRequest
from trading_game.core.book import Book
from trading_game.core.option_pricer import Option, Strategy, Greeks
from trading_game.core.manual_trading import (
    OrderExecutor, VanillaOrder, StrategyOrder,
    OrderSide, OrderType, StrategyType
)
from trading_game.models.stock import Stock
from trading_game.models.street import Street

from trading_game.app.layouts.market_overview import render_market_overview
from trading_game.app.components.metrics import render_top_metrics
from trading_game.app.components.sidebar_header import render_header, render_side_bar
from trading_game.app.utils.styling import remove_st_default, global_theme
from trading_game.app.utils.functions import *



def render_main_layout() -> None:
    # Styling
    remove_st_default()
    global_theme()

    # BAR AND HEADER
    render_side_bar()
    render_header()

    # First computations
    portfolio_value = calculate_total_portfolio_value()
    pnl = portfolio_value - st.session_state.starting_cash
    pnl_pct = (pnl / st.session_state.starting_cash) * 100
    risk_score = calculate_risk_score()
    portfolio_greeks = calculate_portfolio_greeks()

    # METRICS
    render_top_metrics(portfolio_value, pnl, pnl_pct, risk_score)

    # ============================================================================
    # MARKET OVERVIEW
    # ============================================================================
    render_market_overview(pnl, portfolio_greeks)

    # ============================================================================
    # POSITIONS TABLE
    # ============================================================================
    st.markdown('<a id="positions"></a>', unsafe_allow_html=True)
    st.header("📈 Current Positions")

    if st.session_state.positions:
        positions_data = []
        for idx, pos in enumerate(st.session_state.positions):

            # Handle different position types
            if 'strike' in pos:  # Vanilla
                strike = pos['strike']
                option_type = pos['type']
            elif 'strikes' in pos:  # Strategy
                # Example: for call spread, take average strike for valuation
                strike = sum(pos['strikes']) / len(pos['strikes'])
                option_type = pos.get('type', 'strategy')
            else:
                st.warning(f"Skipping position {idx} — no strike info")
                continue

            current_price = black_scholes(
                st.session_state.stock.last_price,
                strike,
                pos['time_to_expiry'],
                0.02,
                0.3,
                pos['type']
            )

            greeks = calculate_greeks(
                st.session_state.stock.last_price,
                strike,
                pos['time_to_expiry'],
                0.02,
                0.3,
                pos['type']
            )

            position_pnl = (current_price - pos['purchase_price']) * pos['quantity'] * 100 * pos['side']

            positions_data.append({
                'ID': idx,
                'Side': 'LONG' if pos['side'] == 1 else 'SHORT',
                'Type': pos['type'].upper(),
                'Strike': (
                    f"${pos['strike']:.0f}" if 'strike' in pos
                    else ", ".join([f"${s:.0f}" for s in pos.get('strikes', [])])
                ),
                'Qty': pos['quantity'],
                'Entry': f"${pos['purchase_price']:.2f}",
                'Current': f"${current_price:.2f}",
                'P&L': f"${position_pnl:.0f}",
                'Delta': f"{greeks['delta'] * pos['quantity'] * 100 * pos['side']:.0f}",
                'Gamma': f"{greeks['gamma'] * pos['quantity'] * 100:.2f}",
                'Expiry': pos['expiry_date'].strftime('%Y-%m-%d'),
                'DTE': int(pos['time_to_expiry'] * 365)
            })

        df_positions = pd.DataFrame(positions_data)
        st.table(df_positions)

        close_col1, close_col2 = st.columns([3, 1])
        with close_col1:
            position_to_close = st.selectbox("Select position to close",
                                             [f"ID {p['ID']} - {p['Type']} {p['Strike']}" for p in positions_data])
        with close_col2:
            if st.button("❌ Close Position", type="primary"):
                idx = int(position_to_close.split()[1])
                pos = st.session_state.positions[idx]
                current_price = black_scholes(
                    st.session_state.stock.last_price,
                    pos['strike'],
                    pos['time_to_expiry'],
                    0.02,
                    0.3,
                    pos['type']
                )
                proceeds = current_price * pos['quantity'] * 100 * pos['side']
                st.session_state.cash += proceeds
                st.session_state.positions.pop(idx)
                st.success(f"Position closed! Proceeds: ${proceeds:.0f}")
                st.rerun()
    else:
        st.info("No open positions")

    st.markdown("### Position")
    fut_col1, fut_col2, fut_col3 = st.columns(3)
    with fut_col1:
        st.metric("Position", f"{st.session_state.futures_position:+.0f} shares")
    with fut_col2:
        if 'futures_entry_price' in st.session_state and st.session_state.futures_position != 0:
            futures_pnl = (
                                      st.session_state.stock.last_price - st.session_state.futures_entry_price) * st.session_state.futures_position
            st.metric("Futures P&L", f"${futures_pnl:,.0f}")
    with fut_col3:
        if st.session_state.futures_position != 0:
            st.metric("Entry Price", f"${st.session_state.get('futures_entry_price', 0):.2f}")

    st.divider()

    # ============================================================================
    # DELTA HEDGING
    # ============================================================================
    st.markdown('<a id="hedging"></a>', unsafe_allow_html=True)
    st.header(f"🛡️ Trading Shares - {st.session_state.stock.ticker}")

    hedge_col1, hedge_col2, hedge_col3 = st.columns([2, 2, 1])

    with hedge_col1:
        st.markdown(f"**Current Portfolio Delta:** {portfolio_greeks['delta']:.0f}")
        recommended_hedge = -portfolio_greeks['delta']
        st.markdown(f"**Recommended Hedge:** {recommended_hedge:+.0f} shares")

    with hedge_col2:
        futures_qty = st.number_input(
            "Stock Quantity",
            min_value=-10000,
            max_value=10000,
            value=int(recommended_hedge),
            step=100,
            help="Positive = Long, Negative = Short"
        )

        futures_cost = abs(futures_qty) * 0.5
        st.caption(f"Transaction cost: ${futures_cost:.2f}")

    with hedge_col3:
        st.write("")
        st.write("")
        if st.button("⚡ Execute Hedge", type="primary"):
            if st.session_state.cash >= futures_cost:
                if st.session_state.futures_position == 0 or np.sign(futures_qty) == np.sign(
                        st.session_state.futures_position):
                    total_position = st.session_state.futures_position + futures_qty
                    if st.session_state.futures_position == 0:
                        st.session_state.futures_entry_price = st.session_state.stock.last_price
                    else:
                        old_notional = st.session_state.futures_position * st.session_state.futures_entry_price
                        new_notional = futures_qty * st.session_state.stock.last_price
                        st.session_state.futures_entry_price = (old_notional + new_notional) / total_position
                    st.session_state.futures_position = total_position
                else:
                    st.session_state.futures_position += futures_qty
                    if st.session_state.futures_position == 0:
                        st.session_state.pop('futures_entry_price', None)

                st.session_state.cash -= futures_cost
                st.success(f"Hedge executed! New position: {st.session_state.futures_position:+.0f}")

                # ADD TRADE TO BOOK
                trade_id = st.session_state.book.add_trade_stock(
                    st.session_state.stock,
                    futures_qty,
                    st.session_state.stock.last_price,
                    st.session_state.stock.last_vol)

                st.rerun()
            else:
                st.error("Insufficient cash for transaction cost!")

    st.divider()

    # ============================================================================
    # CLIENT REQUESTS
    # ============================================================================
    st.markdown('<a id="clients"></a>', unsafe_allow_html=True)
    st.header("📞 Client Requests")

    # Initialize session state for chat history
    if 'quote_chat_history' not in st.session_state:
        st.session_state.quote_chat_history = list()
    if 'pending_quote' not in st.session_state:
        st.session_state.pending_quote = None
    if 'last_quote_tick' not in st.session_state:
        st.session_state.last_quote_tick = 0
    if 'quote_cleared_tick' not in st.session_state:
        st.session_state.quote_cleared_tick = -999

    def add_quote_request(message, quote_id):
        """Add a new quote request to the chat"""
        st.session_state.quote_chat_history.append({
            'type': 'request',
            'message': message,
            'quote_id': quote_id,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.pending_quote = quote_id

    def add_player_response(quote_id, bid, ask):
        """Add player's bid/ask response to the chat"""
        st.session_state.quote_chat_history.append({
            'type': 'player_response',
            'quote_id': quote_id,
            'bid': bid,
            'ask': ask,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })

    def add_market_response(quote_id, final_answer):
        st.session_state.quote_chat_history.append({
            'type': 'market_response',
            'quote_id': quote_id,
            'message': final_answer,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })

        # Process result if exists (add trade to book)
        if st.session_state.result:
            st.session_state.book.add_trade_strategy(
                st.session_state.quote_request.strat,
                st.session_state.quote_request.quantity,
                st.session_state.stock.last_price,
                st.session_state.stock.last_vol)  # check if right spot ref

        st.session_state.quote_cleared_tick = st.session_state.tick_count
        st.session_state.pending_quote = None

    def clear_chat():
        """Clear the chat history"""
        st.session_state.quote_chat_history = list()

    def render_quote_chat():
        # Chat container with custom styling
        chat_container = st.container()

        with chat_container:
            # Display chat history
            for msg in st.session_state.quote_chat_history:
                if msg['type'] == 'request' or msg['type'] == 'market_response':
                    # Quote request from market
                    st.markdown(f"""
                    <div style="background-color: #d0d4db; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%;">
                        <small style="color: #666;">{msg['timestamp']}</small><br>
                        {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
                elif msg['type'] == 'player_response':
                    # Player's response
                    st.markdown(f"""
                    <div style="background-color: #a8d5a8; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%; margin-left: auto;">
                        <small style="color: #666;">{msg['timestamp']}</small><br>
                        <strong>You:</strong> Bid: ${msg['bid']:.2f} / Ask: ${msg['ask']:.2f}
                    </div>
                    """, unsafe_allow_html=True)

        # Input section for pending quote
        if st.session_state.pending_quote is not None:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                bid_price = st.number_input("Your Bid ($)", min_value=0.0, step=0.05, format="%.2f",
                                            key=f"bid_{st.session_state.pending_quote}")

            with col2:
                ask_price = st.number_input("Your Ask ($)", min_value=0.0, step=0.05, format="%.2f",
                                            key=f"ask_{st.session_state.pending_quote}")

            with col3:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacer
                if st.button("Send Quote", type="primary", use_container_width=True):
                    if ask_price <= bid_price:
                        st.error("Ask must be higher than Bid!")
                    else:
                        # Add player response to chat
                        add_player_response(st.session_state.pending_quote, bid_price, ask_price)
                        # Evaluate response
                        result = st.session_state.quote_request.evaluate_bid_ask(bid_price, ask_price,
                                                                                 st.session_state.stock.last_price,
                                                                                 st.session_state.stock.last_vol)
                        st.session_state.result = result
                        final_answer = st.session_state.quote_request.generate_response_message(result)
                        # Add market response to chat
                        add_market_response(st.session_state.pending_quote, final_answer)

                        st.rerun()
        else:
            st.info("No pending quote requests. Keep trading!")

    # Initialize session state variables for quote requests
    if "quote_request" not in st.session_state:
        st.session_state.quote_request = None
    if "quote_request_history" not in st.session_state:
        st.session_state.quote_request_history = list()
    if "result" not in st.session_state:
        st.session_state.result = None

    # Quote request management based on tick_count
    def manage_quote_requests(current_tick):
        """
        Manages the timing of quote requests
        current_tick: the current tick count from st.session_state.tick_count
        """

        # Clear chat one tick after market response
        if current_tick == st.session_state.quote_cleared_tick + 2:
            clear_chat()

            # Reset for next quote
            st.session_state.quote_request = None
            st.session_state.result = None

        # Check if it's time for a new quote request
        # First quote at tick 3, then every 3 ticks after previous quote
        if current_tick == 3 and st.session_state.last_quote_tick == 0:
            # First quote request
            investor = random.choice(st.session_state.street.investors)
            level = 'easy' if len(st.session_state.quote_request_history) <= 3 else 'hard'
            quote_request = QuoteRequest(investor=investor, level=level, init_price=st.session_state.stock.last_price)
            st.session_state.quote_request = quote_request
            st.session_state.quote_request_history.append(quote_request)

            quote_id = f"q_{current_tick}"
            message = quote_request.generate_request_message()
            add_quote_request(message, quote_id)
            st.session_state.last_quote_tick = current_tick

        elif (st.session_state.quote_cleared_tick > 0 and
              current_tick == st.session_state.quote_cleared_tick + 3):
            # New quote request 3 ticks after the last one was cleared
            investor = random.choice(st.session_state.street.investors)
            level = 'easy' if len(st.session_state.quote_request_history) <= 3 else 'hard'
            quote_request = QuoteRequest(investor=investor, level=level, init_price=st.session_state.stock.last_price)
            st.session_state.quote_request = quote_request
            st.session_state.quote_request_history.append(quote_request)

            quote_id = f"q_{current_tick}"
            message = quote_request.generate_request_message()
            add_quote_request(message, quote_id)
            st.session_state.last_quote_tick = current_tick

    # Manage quote requests based on current tick
    if 'tick_count' in st.session_state:
        manage_quote_requests(st.session_state.tick_count)

    render_quote_chat()

    st.divider()

    # ============================================================================
    # MANUAL TRADING
    # ============================================================================
    st.markdown('<a name="manual-trading"></a>', unsafe_allow_html=True)
    st.header(f"💼 Trading Options - {st.session_state.stock.ticker}")
    tab1, tab2 = st.tabs(["Vanilla Options", "Strategies"])

    # ===== TAB 1: VANILLA OPTIONS =====
    with tab1:
        st.markdown("#### Buy/Sell Vanilla Options")

        col1, col2 = st.columns(2)

        with col1:
            side = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="vanilla_side")
            option_type = st.selectbox("Type", ["call", "put"], key="vanilla_type")
            strike = st.number_input(
                "Strike",
                value=float(st.session_state.stock.last_price),
                step=5.0,
                key="vanilla_strike"
            )

        with col2:
            days = st.slider("Days to Expiry", 1, 365, 30, key="vanilla_dte")
            qty = st.number_input("Quantity", min_value=1, value=1, key="vanilla_qty")
            order_type_choice = st.radio(
                "Order Type", ["Market", "Limit"], horizontal=True, key="vanilla_order_type"
            )

            if order_type_choice == "Limit":
                limit_price = st.number_input(
                    "Limit Price", min_value=0.01, value=1.0, step=0.1, key="vanilla_limit"
                )
            else:
                limit_price = None

        if st.button("Execute Vanilla Trade", key="btn_vanilla"):
            vanilla_order = VanillaOrder(
                side=OrderSide.BUY if side == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_choice == "Market" else OrderType.LIMIT,
                quantity=qty,
                option_type=option_type,
                strike=strike,
                maturity=days / 365,
                spot_price=st.session_state.stock.last_price,
                volatility=st.session_state.stock.last_vol,
                risk_free_rate=RF,
                limit_price=limit_price
            )

            submitted = st.session_state.order_executor.submit_order(vanilla_order)
            if submitted:
                success = st.session_state.order_executor.execute_vanilla_order(vanilla_order, Option)

                if success:
                    cost = vanilla_order.executed_price * qty * 100
                    st.session_state.cash += -cost if side == "Buy" else cost
                    st.session_state.positions.append({
                        'type': option_type,
                        'strike': strike,
                        'expiry_date': datetime.now() + timedelta(days=days),
                        'time_to_expiry': days / 365,
                        'quantity': qty,
                        'purchase_price': vanilla_order.executed_price,
                        'side': 1 if side == "Buy" else -1,
                        'order_id': vanilla_order.order_id
                    })
                    st.success(f"✅ {side} order executed at ${vanilla_order.executed_price:.4f}")
                    st.info(f"💰 Total cost: ${cost:.2f}")
                    st.rerun()
                else:
                    st.error("❌ Order could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {vanilla_order.rejection_reason}")

    # ===== TAB 2: STRATEGIES =====
    with tab2:
        st.markdown("#### Execute Option Strategies")

        strat_type = st.selectbox(
            "Strategy Type",
            [
                "Call Spread",
                "Put Spread",
                "Straddle",
                "Strangle",
                "Call Calendar Spread",
                "Put Calendar Spread",
                "Bull Risk Reversal",
                "Bear Risk Reversal",
                "Call Butterfly",
                "Put Butterfly"
            ],
            key="strat_type"
        )

        col1, col2 = st.columns(2)

        with col1:
            side_strat = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="strat_side")

            # ===== 2 STRIKES =====
            if strat_type in [
                "Call Spread",
                "Put Spread",
                "Strangle",
                "Bull Risk Reversal",
                "Bear Risk Reversal"
            ]:
                strike1 = st.number_input(
                    "Strike 1",
                    value=float(st.session_state.stock.last_price * 0.95),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k1"
                )
                strike2 = st.number_input(
                    "Strike 2",
                    value=float(st.session_state.stock.last_price * 1.05),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k2"
                )
                strikes = [strike1, strike2]

            # ===== 3 STRIKES (BUTTERFLIES) =====
            elif strat_type in ["Call Butterfly", "Put Butterfly"]:
                strike1 = st.number_input(
                    "Strike 1 (Low)",
                    value=float(st.session_state.stock.last_price * 0.90),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k1_fly"
                )
                strike2 = st.number_input(
                    "Strike 2 (Mid)",
                    value=float(st.session_state.stock.last_price),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k2_fly"
                )
                strike3 = st.number_input(
                    "Strike 3 (High)",
                    value=float(st.session_state.stock.last_price * 1.10),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k3_fly"
                )
                strikes = [strike1, strike2, strike3]

            # ===== 1 STRIKE (STRADDLE + CALENDARS) =====
            else:  # Straddle, Call Calendar Spread, Put Calendar Spread
                label = "Strike (ATM)" if strat_type == "Straddle" else "Strike"
                strike_atm = st.number_input(
                    label,
                    value=float(st.session_state.stock.last_price),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k"
                )
                strikes = [strike_atm]

        with col2:
            # ---- Maturities ----
            if strat_type in ["Call Calendar Spread", "Put Calendar Spread"]:
                # Deux maturités comme dans ton pricer : short & long
                short_days_strat = st.slider(
                    "Short Leg - Days to Expiry",
                    1, 365, 30,
                    key="strat_dte_short"
                )
                long_days_strat = st.slider(
                    "Long Leg - Days to Expiry",
                    2, 730, 180,
                    key="strat_dte_long"
                )
                # Pour l'instant, on continue à utiliser une seule maturité dans StrategyOrder
                # On prend par exemple la maturité longue pour 'maturity'
                days_strat = long_days_strat
            else:
                days_strat = st.slider(
                    "Days to Expiry",
                    1, 365, 30,
                    key="strat_dte"
                )

            qty_strat = st.number_input("Quantity", min_value=1, value=1, key="strat_qty")
            order_type_strat = st.radio(
                "Order Type", ["Market", "Limit"], horizontal=True, key="strat_order_type"
            )

            if order_type_strat == "Limit":
                limit_price_strat = st.number_input(
                    "Limit Price", min_value=0.01, value=1.0, step=0.1, key="strat_limit"
                )
            else:
                limit_price_strat = None

        if st.button("Execute Strategy", key="btn_strategy"):
            strat_type_map = {
                "Call Spread": StrategyType.CALL_SPREAD,
                "Put Spread": StrategyType.PUT_SPREAD,
                "Straddle": StrategyType.STRADDLE,
                "Strangle": StrategyType.STRANGLE,
                "Call Calendar Spread": StrategyType.CALL_CALENDAR_SPREAD,
                "Put Calendar Spread": StrategyType.PUT_CALENDAR_SPREAD,
                "Bull Risk Reversal": StrategyType.BULL_RISK_REVERSAL,
                "Bear Risk Reversal": StrategyType.BEAR_RISK_REVERSAL,
                "Call Butterfly": StrategyType.CALL_BUTTERFLY,
                "Put Butterfly": StrategyType.PUT_BUTTERFLY,
            }

            strategy_order = StrategyOrder(
                side=OrderSide.BUY if side_strat == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_strat == "Market" else OrderType.LIMIT,
                quantity=qty_strat,
                strategy_type=strat_type_map[strat_type],
                strikes=strikes,
                maturity=days_strat / 365,
                short_maturity=short_days_strat / 365 if strat_type in ["Call Calendar Spread",
                                                                        "Put Calendar Spread"] else None,
                long_maturity=long_days_strat / 365 if strat_type in ["Call Calendar Spread",
                                                                      "Put Calendar Spread"] else None,
                spot_price=st.session_state.stock.last_price,
                volatility=st.session_state.stock.last_vol,
                risk_free_rate=RF,
                limit_price=limit_price_strat
            )

            submitted = st.session_state.order_executor.submit_order(strategy_order)
            if submitted:
                success = st.session_state.order_executor.execute_strategy_order(strategy_order, Strategy)

                if success:
                    cost = strategy_order.net_premium * qty_strat * 100
                    st.session_state.cash += -cost if side_strat == "Buy" else cost
                    st.session_state.positions.append({
                        'type': strat_type,
                        'strikes': strikes,
                        'expiry_date': datetime.now() + timedelta(days=days_strat),
                        'time_to_expiry': days_strat / 365,
                        'quantity': qty_strat,
                        'purchase_price': strategy_order.net_premium,
                        'side': 1 if side_strat == "Buy" else -1,
                        'order_id': strategy_order.order_id
                    })
                    st.success(f"✅ {strat_type} executed at ${strategy_order.net_premium:.4f}")
                    st.info(f"💰 Total cost: ${cost:.2f}")
                    st.rerun()
                else:
                    st.error("❌ Strategy could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {strategy_order.rejection_reason}")

    # ============================================================================
    # CONTROLS
    # ============================================================================
    st.header("🎮 Game Controls")

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        if st.button("⏸️ Pause" if not st.session_state.trading_paused else "▶️ Resume", use_container_width=True,
                     type="primary"):
            st.session_state.trading_paused = not st.session_state.trading_paused
            st.rerun()

    with control_col2:
        if st.button("🔄 Reset Game", use_container_width=True, type="primary"):
            st.session_state.stock = Stock.stock()
            st.session_state.street = Street.street()
            st.session_state.book = Book()
            st.session_state.order_executor = OrderExecutor(max_position_size=1000)
            st.session_state.cash = 100000.0
            st.session_state.starting_cash = 100000.0
            st.session_state.positions = []
            st.session_state.futures_position = 0
            st.session_state.trade_history = []
            st.session_state.pnl_history = [0]
            st.session_state.tick_count = 0
            st.session_state.game_over = False
            st.rerun()

    with control_col3:
        show_history = st.checkbox("📜 Show Trade History", value=True)

    if show_history:
        st.markdown("### 📜 Trade History")

        if st.session_state.trade_history:
            df = pd.DataFrame(st.session_state.trade_history)

            # Colonnes ordonnées si besoin
            cols = ["Time", "Type", "Instrument", "Price", "Quantity", "PnL"]
            df = df[[c for c in cols if c in df.columns]]

            # Mise en forme type order book
            st.dataframe(
                df.style.set_table_styles([
                    {'selector': 'thead th', 'props': [('background-color', '#0e1117'),
                                                       ('color', 'white'),
                                                       ('font-weight', 'bold'),
                                                       ('text-align', 'center')]},
                    {'selector': 'tbody td', 'props': [('text-align', 'center'),
                                                       ('border', '1px solid #2b2b2b')]},
                ]).format({
                    'Price': '{:.2f}',
                    'Quantity': '{:.0f}',
                    'PnL': '{:+.2f}'
                }),
                use_container_width=True,
                height=250
            )
        else:
            st.info("No trades yet")

    # ============================================================================
    # FOOTER
    # ============================================================================

    # ============================================================================
    # PRICER TOOL
    # ============================================================================
    st.markdown('<a id="pricer"></a>', unsafe_allow_html=True)
    st.header("🧮 Options Pricer Tool")

    pricer_tab1, pricer_tab2 = st.tabs(["Vanilla Options", "Strategies"])

    # ============================================================================
    # TAB 1: SINGLE OPTION PRICER
    # ============================================================================
    with pricer_tab1:
        st.subheader("Price a Single Option")

        # ---------- OPTION TYPE SUR UNE LIGNE SEULE ----------
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Option Type</span>",
            unsafe_allow_html=True
        )
        pricer_opt_type = st.selectbox(
            "pricer_opt_type",  # pas de texte, on gère le titre au-dessus
            ["call", "put"],
            key="pricer_opt_type",
            label_visibility="collapsed"
        )

        # On garde spot & rate en caché (market data)
        pricer_spot = float(st.session_state.stock.last_price)
        pricer_rf = RF

        # ---------- INPUTS À GAUCHE / RÉSULTATS À DROITE ----------
        input_col, result_col = st.columns([2, 1])

        # ----- COLONNE GAUCHE : MARKET PARAMETERS -----
        with input_col:
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Market Parameters</span>",
                unsafe_allow_html=True
            )

            # Strike
            st.markdown(
                "<span style='color:white;'>Strike</span>",
                unsafe_allow_html=True
            )
            pricer_strike = st.number_input(
                "pricer_strike",
                value=float(pricer_spot),
                step=1.0,
                key="pricer_strike",
                label_visibility="collapsed"
            )

            # Vol
            st.markdown(
                "<span style='color:white;'>Volatility (σ)</span>",
                unsafe_allow_html=True
            )
            pricer_vol = st.number_input(
                "pricer_vol",
                value=float(st.session_state.stock.last_vol),
                min_value=0.01,
                max_value=2.0,
                step=0.01,
                format="%.4f",
                key="pricer_vol",
                label_visibility="collapsed"
            )

            # Maturity
            st.markdown(
                "<span style='color:white;'>Time to Maturity (years)</span>",
                unsafe_allow_html=True
            )
            pricer_maturity = st.slider("Days to Expiry", 1, 365, 30, key="maturity_dte")

        # ----- COLONNE DROITE : RESULTS + GREEKS -----

        with result_col:
            # Titre "Results"
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Results</span>",
                unsafe_allow_html=True
            )

            pricer_option = Option(
                K=pricer_strike,
                T=pricer_maturity,
                r=pricer_rf,
                option_type=pricer_opt_type
            )

            option_price = pricer_option.price(pricer_spot, pricer_vol)

            # ----- OPTION PRICE EN ROUGE & GRAS -----
            st.markdown(
                "<span style='color:white; font-weight:bold;'>Option Price</span>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:32px; font-weight:bold; color:#ff4b4b;'>"
                f"${option_price:.4f}</div>",
                unsafe_allow_html=True
            )

            # ----- GREEKS OPTIONNELS DANS UN EXPANDER -----
            pricer_greeks = Greeks(option=pricer_option)
            greeks_result = pricer_greeks.all_greeks(pricer_spot, pricer_vol)

            with st.expander("Show Greeks", expanded=False):
                st.markdown(
                    "<span style='color:white; font-weight:bold;'>Greeks</span>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<span style='font-weight:bold;'>Delta:</span> {greeks_result['delta']:.4f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Gamma:</span> {greeks_result['gamma']:.6f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Vega:</span> {greeks_result['vega']:.4f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Theta:</span> {greeks_result['theta']:.6f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Rho:</span> {greeks_result['rho']:.6f}",
                    unsafe_allow_html=True
                )

    st.divider()

    # ============================================================================
    # TAB 2: STRATEGY PRICER
    # ============================================================================
    with pricer_tab2:
        st.subheader("Price an Options Strategy")

        # ---------- STRATEGY TYPE SUR UNE LIGNE SEULE ----------
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Strategy Type</span>",
            unsafe_allow_html=True
        )
        strat_type_label = st.selectbox(
            "strat_type",
            [
                "Call Spread", "Put Spread", "Straddle", "Strangle",
                "Call Calendar Spread", "Put Calendar Spread",
                "Bull Risk Reversal", "Bear Risk Reversal",
                "Call Butterfly", "Put Butterfly",
            ],
            key="strat_pricer_type",
            label_visibility="collapsed"
        )

        # Spot & taux cachés (comme pour la single option)
        strat_spot = float(st.session_state.stock.last_price)
        strat_rf = 0.02

        # ---------- INPUTS À GAUCHE / RÉSULTATS À DROITE ----------
        input_col, result_col = st.columns([2, 1])

        # ===== COLONNE GAUCHE : MARKET + STRIKES =====
        with input_col:
            # ---- Market parameters ----
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Market Parameters</span>",
                unsafe_allow_html=True
            )

            # Vol (avec wrapper vol_green si tu as ajouté le CSS)
            st.markdown(
                "<span style='color:white;'>Volatility (σ)</span>",
                unsafe_allow_html=True
            )
            st.markdown('<div class="vol_green">', unsafe_allow_html=True)
            strat_vol = st.number_input(
                "strat_vol",
                value=float(st.session_state.stock.last_vol),
                min_value=0.01,
                max_value=3.0,
                step=0.01,
                format="%.4f",
                key="strat_pricer_vol",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # ---- Maturité ----
            if strat_type_label in ["Call Calendar Spread", "Put Calendar Spread"]:
                # Deux maturités : short & long
                st.markdown(
                    "<span style='color:white;'>Short Leg – Days to Expiry</span>",
                    unsafe_allow_html=True
                )
                strat_short_days = st.slider(
                    "strat_short_days",
                    min_value=1,
                    max_value=365,
                    value=30,
                    key="strat_pricer_dte_short",
                    label_visibility="collapsed"
                )
                st.markdown(
                    "<span style='color:white;'>Long Leg – Days to Expiry</span>",
                    unsafe_allow_html=True
                )
                strat_long_days = st.slider(
                    "strat_long_days",
                    min_value=2,
                    max_value=730,
                    value=180,
                    key="strat_pricer_dte_long",
                    label_visibility="collapsed"
                )
                t_short = strat_short_days / 365.0
                t_long = strat_long_days / 365.0
            else:
                st.markdown(
                    "<span style='color:white;'>Days to Expiry</span>",
                    unsafe_allow_html=True
                )
                strat_maturity_days = st.slider(
                    "strat_mat_days",
                    min_value=1,
                    max_value=365,
                    value=30,
                    key="strat_pricer_dte",
                    label_visibility="collapsed"
                )
                strat_maturity = strat_maturity_days / 365.0  # en années

            # ---- Strikes ----
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Strikes</span>",
                unsafe_allow_html=True
            )

            # 1 strike : Straddle + Calendar spreads
            if strat_type_label in ["Straddle", "Call Calendar Spread", "Put Calendar Spread"]:
                label_strike = "Strike (ATM)" if strat_type_label == "Straddle" else "Strike"
                st.markdown(
                    f"<span style='color:white;'>{label_strike}</span>",
                    unsafe_allow_html=True
                )
                strat_k = st.number_input(
                    "strat_k",
                    value=float(strat_spot),
                    step=1.0,
                    key="strat_pricer_k",
                    label_visibility="collapsed"
                )

            # 2 strikes : spreads, strangle, risk reversals
            elif strat_type_label in [
                "Call Spread", "Put Spread", "Strangle",
                "Bull Risk Reversal", "Bear Risk Reversal"
            ]:
                st.markdown(
                    "<span style='color:white;'>Strike 1</span>",
                    unsafe_allow_html=True
                )
                strat_k1 = st.number_input(
                    "strat_k1",
                    value=float(strat_spot - 5),
                    step=1.0,
                    key="strat_pricer_k1",
                    label_visibility="collapsed"
                )

                st.markdown(
                    "<span style='color:white;'>Strike 2</span>",
                    unsafe_allow_html=True
                )
                strat_k2 = st.number_input(
                    "strat_k2",
                    value=float(strat_spot + 5),
                    step=1.0,
                    key="strat_pricer_k2",
                    label_visibility="collapsed"
                )

            # 3 strikes : butterflies
            elif strat_type_label in ["Call Butterfly", "Put Butterfly"]:
                st.markdown(
                    "<span style='color:white;'>Strike 1 (Low)</span>",
                    unsafe_allow_html=True
                )
                strat_k1_fly = st.number_input(
                    "strat_k1_fly",
                    value=float(strat_spot - 10),
                    step=1.0,
                    key="strat_pricer_k1_fly",
                    label_visibility="collapsed"
                )

                st.markdown(
                    "<span style='color:white;'>Strike 2 (Mid)</span>",
                    unsafe_allow_html=True
                )
                strat_k2_fly = st.number_input(
                    "strat_k2_fly",
                    value=float(strat_spot),
                    step=1.0,
                    key="strat_pricer_k2_fly",
                    label_visibility="collapsed"
                )

                st.markdown(
                    "<span style='color:white;'>Strike 3 (High)</span>",
                    unsafe_allow_html=True
                )
                strat_k3_fly = st.number_input(
                    "strat_k3_fly",
                    value=float(strat_spot + 10),
                    step=1.0,
                    key="strat_pricer_k3_fly",
                    label_visibility="collapsed"
                )

        # ===== COLONNE DROITE : RESULTS + GREEKS =====
        with result_col:
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Results</span>",
                unsafe_allow_html=True
            )

            # Construction de la stratégie en fonction du type choisi
            if strat_type_label == "Call Spread":
                strategy = Strategy.call_spread(
                    k1=strat_k1,
                    k2=strat_k2,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Put Spread":
                strategy = Strategy.put_spread(
                    k1=strat_k1,
                    k2=strat_k2,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Straddle":
                strategy = Strategy.straddle(
                    k=strat_k,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Strangle":
                strategy = Strategy.strangle(
                    k1=strat_k1,
                    k2=strat_k2,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Call Calendar Spread":
                strategy = Strategy.calendar_spread(
                    k=strat_k,
                    t1=t_short,
                    t2=t_long,
                    r=strat_rf,
                    option_type="call"
                )
            elif strat_type_label == "Put Calendar Spread":
                strategy = Strategy.calendar_spread(
                    k=strat_k,
                    t1=t_short,
                    t2=t_long,
                    r=strat_rf,
                    option_type="put"
                )
            elif strat_type_label == "Bull Risk Reversal":
                strategy = Strategy.risk_reversal_bullish(
                    k1=strat_k1,
                    k2=strat_k2,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Bear Risk Reversal":
                strategy = Strategy.risk_reversal_bearish(
                    k1=strat_k1,
                    k2=strat_k2,
                    t=strat_maturity,
                    r=strat_rf
                )
            elif strat_type_label == "Call Butterfly":
                strategy = Strategy.butterfly(
                    k1=strat_k1_fly,
                    k2=strat_k2_fly,
                    k3=strat_k3_fly,
                    t=strat_maturity,
                    r=strat_rf,
                    option_type="call"
                )
            elif strat_type_label == "Put Butterfly":
                strategy = Strategy.butterfly(
                    k1=strat_k1_fly,
                    k2=strat_k2_fly,
                    k3=strat_k3_fly,
                    t=strat_maturity,
                    r=strat_rf,
                    option_type="put"
                )

            # ----- STRATEGY PRICE EN ROUGE & GRAS -----
            strategy_price = strategy.price(strat_spot, strat_vol)
            st.markdown(
                "<span style='color:white; font-weight:bold;'>Strategy Price</span>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:32px; font-weight:bold; color:#ff4b4b;'>"
                f"${strategy_price:.4f}</div>",
                unsafe_allow_html=True
            )

            # ----- GREEKS OPTIONNELS DANS UN EXPANDER -----
            strat_greeks_calc = Greeks(strategy=strategy)
            strat_greeks = strat_greeks_calc.all_greeks(strat_spot, strat_vol)

            with st.expander("Show Greeks", expanded=False):
                st.markdown(
                    "<span style='color:white; font-weight:bold;'>Greeks</span>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<span style='font-weight:bold;'>Delta:</span> {strat_greeks['delta']:.4f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Gamma:</span> {strat_greeks['gamma']:.6f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Vega:</span> {strat_greeks['vega']:.4f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Theta:</span> {strat_greeks['theta']:.6f}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-weight:bold;'>Rho:</span> {strat_greeks['rho']:.6f}",
                    unsafe_allow_html=True
                )
