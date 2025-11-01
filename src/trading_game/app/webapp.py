import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh

from trading_game.config.settings import REFRESH_INTERVAL
from trading_game.core.market import Stock

# ============================================================================
# PAGE CONFIG - Dark Theme
# ============================================================================
st.set_page_config(
    page_title="Options Market Maker", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2e3444;
    }
    .risk-high {
        color: #ff4444 !important;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffaa00 !important;
    }
    .risk-low {
        color: #00ff88 !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
    .nav-link {
        display: block;
        padding: 10px;
        margin: 5px 0;
        background-color: #1e2130;
        border-radius: 5px;
        text-decoration: none;
        color: white;
        text-align: center;
        transition: background-color 0.3s;
    }
    .nav-link:hover {
        background-color: #2e3444;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE FIRST (before auto-refresh!)
# ============================================================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.stock = Stock(name="alphabet", ticker="abc", sector="tech", vol=0.3)
    #st.session_state.current_price = 100.0
    # st.session_state.price_history = [100.0]
    # st.session_state.time_history = [datetime.now()]
    st.session_state.cash = 100000.0
    st.session_state.starting_cash = 100000.0
    st.session_state.positions = []
    st.session_state.futures_position = 0
    st.session_state.trade_history = []
    st.session_state.pnl_history = [0]
    st.session_state.game_duration = 150
    st.session_state.tick_count = 0
    st.session_state.game_over = False
    st.session_state.trading_paused = False

# CRITICAL: Initialize new attributes for existing sessions
if 'game_duration' not in st.session_state:
    st.session_state.game_duration = 150
if 'tick_count' not in st.session_state:
    st.session_state.tick_count = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'trading_paused' not in st.session_state:
    st.session_state.trading_paused = False

# Auto-refresh (AFTER initialization)
if not st.session_state.trading_paused and not st.session_state.game_over:
    count = st_autorefresh(interval=REFRESH_INTERVAL, key="price_refresh")

# ============================================================================
# PRICING FUNCTIONS (Placeholders pour votre pricer)
# ============================================================================
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """Black-Scholes pricer - À remplacer par votre pricer"""
    if T <= 0:
        if option_type == 'call':
            return max(0, S - K)
        else:
            return max(0, K - S)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return price

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate Greeks - À adapter selon votre pricer"""
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) / 365
    
    return {'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega}

def get_bid_ask_spread(option_price, volatility=0.3):
    """
    PLACEHOLDER - À remplacer par votre fonction de spread
    Retourne (bid, ask) basé sur le mid price
    """
    spread = option_price * 0.02
    bid = option_price - spread/2
    ask = option_price + spread/2
    return bid, ask

def simulate_price_movement(current_price, dt=1/252, mu=0.05, sigma=0.3):
    """GBM simulation"""
    shock = np.random.normal(0, 1)
    drift = (mu - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * shock
    new_price = current_price * np.exp(drift + diffusion)
    return new_price

# ============================================================================
# RISK CALCULATIONS
# ============================================================================
def calculate_portfolio_greeks():
    """Calculate aggregated Greeks across all positions"""
    total_delta = st.session_state.futures_position
    total_gamma = 0
    total_vega = 0
    total_theta = 0
    
    for pos in st.session_state.positions:
        greeks = calculate_greeks(
            st.session_state.stock.last_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        
        multiplier = pos['quantity'] * 100 * pos['side']
        total_delta += greeks['delta'] * multiplier
        total_gamma += greeks['gamma'] * multiplier
        total_vega += greeks['vega'] * multiplier
        total_theta += greeks['theta'] * multiplier
    
    return {
        'delta': total_delta,
        'gamma': total_gamma,
        'vega': total_vega,
        'theta': total_theta
    }

def calculate_total_portfolio_value():
    """Calculate total portfolio value"""
    total = st.session_state.cash
    
    for pos in st.session_state.positions:
        option_price = black_scholes(
            st.session_state.stock.last_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        total += option_price * pos['quantity'] * 100 * pos['side']
    
    if 'futures_entry_price' in st.session_state and st.session_state.futures_position != 0:
        futures_pnl = (st.session_state.stock.last_price - st.session_state.futures_entry_price) * st.session_state.futures_position
        total += futures_pnl
    
    return total

def calculate_risk_score():
    """Risk score based on delta, gamma, and P&L"""
    greeks = calculate_portfolio_greeks()
    portfolio_value = calculate_total_portfolio_value()
    
    delta_risk = abs(greeks['delta']) / 1000
    gamma_risk = abs(greeks['gamma']) / 100
    
    pnl = portfolio_value - st.session_state.starting_cash
    pnl_score = max(0, pnl / st.session_state.starting_cash * 100)
    
    score = max(0, 100 - delta_risk * 30 - gamma_risk * 20 + pnl_score * 50)
    
    return min(100, score)

# ============================================================================
# UPDATE PRICE
# ============================================================================
if not st.session_state.trading_paused and not st.session_state.game_over:
    if st.session_state.tick_count >= st.session_state.game_duration:
        st.session_state.game_over = True
    else:
        st.session_state.stock.move_price()
        # st.session_state.current_price = simulate_price_movement(st.session_state.current_price)
        # st.session_state.price_history.append(st.session_state.current_price)
        # st.session_state.time_history.append(datetime.now())
        st.session_state.tick_count += 1
        
        total_pnl = calculate_total_portfolio_value() - st.session_state.starting_cash
        st.session_state.pnl_history.append(total_pnl)
        
        for pos in st.session_state.positions:
            time_remaining = (pos['expiry_date'] - datetime.now()).total_seconds() / (365 * 24 * 3600)
            pos['time_to_expiry'] = max(0, time_remaining)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.title("🧭 Navigation")
    st.markdown("---")
    
    st.markdown("""
    <a href="#market-overview" class="nav-link">📊 Market Overview</a>
    <a href="#risk-dashboard" class="nav-link">⚠️ Risk Dashboard</a>
    <a href="#positions" class="nav-link">📈 Positions</a>
    <a href="#hedging" class="nav-link">🛡️ Delta Hedging</a>
    <a href="#clients" class="nav-link">📞 Client Requests</a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    new_duration = st.slider(
        "Game Duration (ticks)", 
        min_value=50, 
        max_value=300, 
        value=st.session_state.game_duration,
        help="Adjust game length"
    )
    if new_duration != st.session_state.game_duration and st.session_state.tick_count == 0:
        st.session_state.game_duration = new_duration
    
    st.caption(f"⏱️ Refresh: 1.5s")
    st.caption(f"🎮 Status: {'PAUSED' if st.session_state.trading_paused else 'ACTIVE'}")
    st.caption(f"🏁 Game: {'OVER' if st.session_state.game_over else 'IN PROGRESS'}")

# ============================================================================
# HEADER
# ============================================================================
st.title("🎯 Options Market Maker Dashboard")

if st.session_state.game_over:
    final_pnl = calculate_total_portfolio_value() - st.session_state.starting_cash
    final_score = calculate_risk_score()
    
    if final_pnl > 0:
        st.success(f"🎉 GAME OVER - YOU WIN! Final P&L: ${final_pnl:,.0f} | Score: {final_score:.0f}/100")
    else:
        st.error(f"💀 GAME OVER - Better luck next time! Final P&L: ${final_pnl:,.0f} | Score: {final_score:.0f}/100")
    st.divider()

progress_pct = st.session_state.tick_count / st.session_state.game_duration
time_remaining = st.session_state.game_duration - st.session_state.tick_count

col_progress1, col_progress2 = st.columns([4, 1])
with col_progress1:
    st.progress(progress_pct, text=f"Game Progress: {st.session_state.tick_count}/{st.session_state.game_duration} ticks")
with col_progress2:
    st.metric("Time Left", f"{time_remaining} ticks")

st.divider()

# ============================================================================
# TOP METRICS
# ============================================================================
portfolio_value = calculate_total_portfolio_value()
pnl = portfolio_value - st.session_state.starting_cash
pnl_pct = (pnl / st.session_state.starting_cash) * 100
risk_score = calculate_risk_score()
portfolio_greeks = calculate_portfolio_greeks()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Underlying Price", 
        f"${st.session_state.stock.last_price:.2f}",
        delta=f"{st.session_state.stock.last_price - st.session_state.stock.price_history[-2]:.2f}" if len(st.session_state.stock.price_history) > 1 else None
    )

with col2:
    st.metric(
        "Portfolio Value", 
        f"${portfolio_value:,.0f}",
        delta=f"{pnl_pct:.2f}%"
    )

with col3:
    st.metric("P&L", f"${pnl:,.0f}", delta=f"{pnl_pct:.1f}%")

with col4:
    st.metric("Cash", f"${st.session_state.cash:,.0f}")

with col5:
    score_color = "🟢" if risk_score > 70 else "🟡" if risk_score > 40 else "🔴"
    st.metric("Risk Score", f"{score_color} {risk_score:.0f}/100")

st.divider()

# ============================================================================
# MARKET OVERVIEW
# ============================================================================
st.markdown('<a id="market-overview"></a>', unsafe_allow_html=True)
st.header("📊 Market Overview")

chart_col, risk_col = st.columns([2, 1])

with chart_col:
    st.subheader("📈 Live Stock Price")
    
    fig = go.Figure()
    x_values = list(range(len(st.session_state.stock.price_history)))
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=st.session_state.stock.price_history,
        mode='lines',
        name='Underlying',
        line=dict(color='#00d4ff', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.15)'
    ))
    
    if not st.session_state.game_over:
        fig.add_vline(
            x=st.session_state.tick_count, 
            line_dash="dash", 
            line_color="#ffaa00",
            opacity=0.5
        )
    
    fig.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#2e3444',
            title="Time (ticks)",
            range=[0, st.session_state.game_duration],
            zeroline=True,
            zerolinecolor='#2e3444'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#2e3444', 
            title="Price ($)",
            zeroline=False
        ),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💰 P&L Evolution")
    
    fig_pnl = go.Figure()
    
    fig_pnl.add_trace(go.Scatter(
        x=x_values,
        y=st.session_state.pnl_history,
        mode='lines',
        name='P&L',
        line=dict(color='#00ff88' if pnl > 0 else '#ff4444', width=2.5),
        fill='tozeroy',
        fillcolor=f'rgba(0, 255, 136, 0.15)' if pnl > 0 else 'rgba(255, 68, 68, 0.15)'
    ))
    
    if not st.session_state.game_over:
        fig_pnl.add_vline(
            x=st.session_state.tick_count, 
            line_dash="dash", 
            line_color="#ffaa00",
            opacity=0.5
        )
    
    fig_pnl.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#2e3444',
            title="Time (ticks)",
            range=[0, st.session_state.game_duration],
            zeroline=True,
            zerolinecolor='#2e3444'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#2e3444', 
            title="P&L ($)",
            zeroline=True,
            zerolinecolor='#ffaa00'
        ),
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_pnl, use_container_width=True)

with risk_col:
    st.markdown('<a id="risk-dashboard"></a>', unsafe_allow_html=True)
    st.subheader("⚠️ Risk Dashboard")
    
    def get_risk_color(value, thresholds):
        abs_val = abs(value)
        if abs_val < thresholds[0]:
            return "#00ff88"
        elif abs_val < thresholds[1]:
            return "#ffaa00"
        else:
            return "#ff4444"
    
    st.markdown("### Portfolio Greeks")
    
    delta_color = get_risk_color(portfolio_greeks['delta'], [500, 1500])
    st.markdown(f"**Delta:** <span style='color:{delta_color}; font-size:24px'>{portfolio_greeks['delta']:.0f}</span>", unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['delta']) / 2000))
    
    gamma_color = get_risk_color(portfolio_greeks['gamma'], [50, 150])
    st.markdown(f"**Gamma:** <span style='color:{gamma_color}; font-size:24px'>{portfolio_greeks['gamma']:.2f}</span>", unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['gamma']) / 200))
    
    vega_color = get_risk_color(portfolio_greeks['vega'], [1000, 3000])
    st.markdown(f"**Vega:** <span style='color:{vega_color}; font-size:24px'>{portfolio_greeks['vega']:.0f}</span>", unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['vega']) / 5000))
    
    theta_color = get_risk_color(portfolio_greeks['theta'], [50, 150])
    st.markdown(f"**Theta:** <span style='color:{theta_color}; font-size:24px'>{portfolio_greeks['theta']:.2f}</span>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### Risk Alerts")
    if abs(portfolio_greeks['delta']) > 1500:
        st.error(f"⚠️ High Delta Exposure: {portfolio_greeks['delta']:.0f}")
    if abs(portfolio_greeks['gamma']) > 150:
        st.warning(f"⚠️ High Gamma Risk: {portfolio_greeks['gamma']:.2f}")
    if len(st.session_state.positions) == 0:
        st.info("✅ No positions - No risk")

st.divider()

# ============================================================================
# POSITIONS TABLE
# ============================================================================
st.markdown('<a id="positions"></a>', unsafe_allow_html=True)
st.header("📈 Current Positions")

if st.session_state.positions:
    positions_data = []
    for idx, pos in enumerate(st.session_state.positions):
        current_price = black_scholes(
            st.session_state.stock.last_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        
        greeks = calculate_greeks(
            st.session_state.stock.last_price,
            pos['strike'],
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
            'Strike': f"${pos['strike']:.0f}",
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
    st.dataframe(df_positions, use_container_width=True, hide_index=True)
    
    close_col1, close_col2 = st.columns([3, 1])
    with close_col1:
        position_to_close = st.selectbox("Select position to close", [f"ID {p['ID']} - {p['Type']} {p['Strike']}" for p in positions_data])
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

st.markdown("### Futures Position")
fut_col1, fut_col2, fut_col3 = st.columns(3)
with fut_col1:
    st.metric("Futures Position", f"{st.session_state.futures_position:+.0f} shares")
with fut_col2:
    if 'futures_entry_price' in st.session_state and st.session_state.futures_position != 0:
        futures_pnl = (st.session_state.stock.last_price - st.session_state.futures_entry_price) * st.session_state.futures_position
        st.metric("Futures P&L", f"${futures_pnl:,.0f}")
with fut_col3:
    if st.session_state.futures_position != 0:
        st.metric("Entry Price", f"${st.session_state.get('futures_entry_price', 0):.2f}")

st.divider()

# ============================================================================
# DELTA HEDGING
# ============================================================================
st.markdown('<a id="hedging"></a>', unsafe_allow_html=True)
st.header("🛡️ Delta Hedging (Futures)")

hedge_col1, hedge_col2, hedge_col3 = st.columns([2, 2, 1])

with hedge_col1:
    st.markdown(f"**Current Portfolio Delta:** {portfolio_greeks['delta']:.0f}")
    recommended_hedge = -portfolio_greeks['delta']
    st.markdown(f"**Recommended Hedge:** {recommended_hedge:+.0f} futures")

with hedge_col2:
    futures_qty = st.number_input(
        "Futures Quantity", 
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
            if st.session_state.futures_position == 0 or np.sign(futures_qty) == np.sign(st.session_state.futures_position):
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
            st.rerun()
        else:
            st.error("Insufficient cash for transaction cost!")

st.divider()

# ============================================================================
# CLIENT REQUESTS
# ============================================================================
st.markdown('<a id="clients"></a>', unsafe_allow_html=True)
st.header("📞 Client Requests")
st.info("🔌 **PLACEHOLDER** - Section pour brancher le code de génération des requests clients")

with st.expander("💡 Example Interface"):
    req_col1, req_col2, req_col3 = st.columns(3)
    with req_col1:
        st.markdown("**Client Request #1**")
        st.write("Type: Call Spread")
        st.write("Strikes: 100/110")
        st.write("Quantity: 50")
    with req_col2:
        st.write("**Your Quote:**")
        st.write("Bid: $X.XX")
        st.write("Ask: $X.XX")
    with req_col3:
        st.button("Accept Bid")
        st.button("Accept Ask")

st.divider()

# ============================================================================
# CONTROLS
# ============================================================================
st.header("🎮 Game Controls")

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    if st.button("⏸️ Pause" if not st.session_state.trading_paused else "▶️ Resume", use_container_width=True):
        st.session_state.trading_paused = not st.session_state.trading_paused
        st.rerun()

with control_col2:
    if st.button("🔄 Reset Game", use_container_width=True):
        #st.session_state.last_price = 100.0
        #st.session_state.price_history = [100.0]
        #st.session_state.time_history = [datetime.now()]
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
    show_history = st.checkbox("📜 Show Trade History", value=False)

if show_history:
    with st.expander("📜 Trade History", expanded=True):
        if st.session_state.trade_history:
            df = pd.DataFrame(st.session_state.trade_history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No trades yet")

# ============================================================================
# MANUAL TRADING (for testing - can be removed later)
# ============================================================================
with st.expander("🧪 Manual Trading (Testing Only)"):
    test_col1, test_col2 = st.columns(2)
    
    with test_col1:
        st.markdown("#### Buy/Sell Options")
        side = st.radio("Side", ["Long", "Short"], horizontal=True)
        option_type = st.selectbox("Type", ["call", "put"])
        strike = st.number_input("Strike", value=100.0, step=5.0)
        days = st.slider("DTE", 1, 90, 30)
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button("Execute Trade"):
            price = black_scholes(st.session_state.stock.last_price, strike, days/365, 0.02, 0.3, option_type)
            cost = price * qty * 100
            
            if side == "Long" and st.session_state.cash >= cost:
                st.session_state.cash -= cost
                st.session_state.positions.append({
                    'type': option_type,
                    'strike': strike,
                    'expiry_date': datetime.now() + timedelta(days=days),
                    'time_to_expiry': days/365,
                    'quantity': qty,
                    'purchase_price': price,
                    'side': 1
                })
                st.success("Long position opened!")
                st.rerun()
            elif side == "Short":
                st.session_state.cash += cost
                st.session_state.positions.append({
                    'type': option_type,
                    'strike': strike,
                    'expiry_date': datetime.now() + timedelta(days=days),
                    'time_to_expiry': days/365,
                    'quantity': qty,
                    'purchase_price': price,
                    'side': -1
                })
                st.success("Short position opened!")
                st.rerun()