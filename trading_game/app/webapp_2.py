import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh

# 
============================================================================
# PAGE CONFIG - Dark Theme
# 
============================================================================
st.set_page_config(
    page_title="Options Market Maker", 
    layout="wide",
    initial_sidebar_state="collapsed"
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
</style>
""", unsafe_allow_html=True)

# Auto-refresh
if 'trading_paused' not in st.session_state:
    st.session_state.trading_paused = False

if not st.session_state.trading_paused:
    count = st_autorefresh(interval=1500, key="price_refresh")

# 
============================================================================
# INITIALIZE SESSION STATE
# 
============================================================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_price = 100.0
    st.session_state.price_history = [100.0]
    st.session_state.time_history = [datetime.now()]
    st.session_state.cash = 100000.0
    st.session_state.starting_cash = 100000.0
    st.session_state.positions = []  # Options positions
    st.session_state.futures_position = 0  # Net futures position
    st.session_state.trade_history = []
    st.session_state.pnl_history = [0]

# 
============================================================================
# PRICING FUNCTIONS (Placeholders pour votre pricer)
# 
============================================================================
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """Black-Scholes pricer - À remplacer par votre pricer"""
    if T <= 0:
        if option_type == 'call':
            return max(0, S - K)
        else:
            return max(0, K - S)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * 
np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * 
norm.cdf(-d1)
    
    return price

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate Greeks - À adapter selon votre pricer"""
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * 
np.sqrt(T))
    
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) / 365
    
    return {'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': 
vega}

def get_bid_ask_spread(option_price, volatility=0.3):
    """
    PLACEHOLDER - À remplacer par votre fonction de spread
    Retourne (bid, ask) basé sur le mid price
    """
    spread = option_price * 0.02  # 2% spread de base
    bid = option_price - spread/2
    ask = option_price + spread/2
    return bid, ask

def simulate_price_movement(current_price, dt=1/252, mu=0.05, 
sigma=0.3):
    """GBM simulation"""
    shock = np.random.normal(0, 1)
    drift = (mu - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * shock
    new_price = current_price * np.exp(drift + diffusion)
    return new_price

# 
============================================================================
# RISK CALCULATIONS
# 
============================================================================
def calculate_portfolio_greeks():
    """Calculate aggregated Greeks across all positions"""
    total_delta = st.session_state.futures_position  # Futures delta
    total_gamma = 0
    total_vega = 0
    total_theta = 0
    
    for pos in st.session_state.positions:
        greeks = calculate_greeks(
            st.session_state.current_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        
        multiplier = pos['quantity'] * 100 * pos['side']  # side: 1 
for long, -1 for short
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
    
    # Options value
    for pos in st.session_state.positions:
        option_price = black_scholes(
            st.session_state.current_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        total += option_price * pos['quantity'] * 100 * pos['side']
    
    # Futures P&L (mark-to-market)
    if 'futures_entry_price' in st.session_state:
        futures_pnl = (st.session_state.current_price - 
st.session_state.futures_entry_price) * 
st.session_state.futures_position
        total += futures_pnl
    
    return total

def calculate_risk_score():
    """
    Risk score basé sur:
    - Delta exposure (plus c'est proche de 0, mieux c'est)
    - Gamma (volatilité du delta)
    - Drawdown
    """
    greeks = calculate_portfolio_greeks()
    portfolio_value = calculate_total_portfolio_value()
    
    # Delta risk (normalized)
    delta_risk = abs(greeks['delta']) / 1000  # Penalize delta far 
from 0
    
    # Gamma risk
    gamma_risk = abs(greeks['gamma']) / 100
    
    # P&L component
    pnl = portfolio_value - st.session_state.starting_cash
    pnl_score = max(0, pnl / st.session_state.starting_cash * 100)
    
    # Final score (0-100)
    score = max(0, 100 - delta_risk * 30 - gamma_risk * 20 + 
pnl_score * 50)
    
    return min(100, score)

# 
============================================================================
# UPDATE PRICE
# 
============================================================================
if not st.session_state.trading_paused:
    st.session_state.current_price = 
simulate_price_movement(st.session_state.current_price)
    
st.session_state.price_history.append(st.session_state.current_price)
    st.session_state.time_history.append(datetime.now())
    
    # Track P&L history
    total_pnl = calculate_total_portfolio_value() - 
st.session_state.starting_cash
    st.session_state.pnl_history.append(total_pnl)
    
    if len(st.session_state.price_history) > 100:
        st.session_state.price_history = 
st.session_state.price_history[-100:]
        st.session_state.time_history = 
st.session_state.time_history[-100:]
        st.session_state.pnl_history = 
st.session_state.pnl_history[-100:]
    
    # Update time to expiry for all positions
    for pos in st.session_state.positions:
        time_remaining = (pos['expiry_date'] - 
datetime.now()).total_seconds() / (365 * 24 * 3600)
        pos['time_to_expiry'] = max(0, time_remaining)

# 
============================================================================
# HEADER - KPIs
# 
============================================================================
st.title("🎯 Options Market Maker Dashboard")

# Calculate metrics
portfolio_value = calculate_total_portfolio_value()
pnl = portfolio_value - st.session_state.starting_cash
pnl_pct = (pnl / st.session_state.starting_cash) * 100
risk_score = calculate_risk_score()
portfolio_greeks = calculate_portfolio_greeks()

# Top metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Underlying Price", 
        f"${st.session_state.current_price:.2f}",
        delta=f"{st.session_state.current_price - 
st.session_state.price_history[-2]:.2f}" if 
len(st.session_state.price_history) > 1 else None
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
    score_color = "🟢" if risk_score > 70 else "🟡" if risk_score > 
40 else "🔴"
    st.metric("Risk Score", f"{score_color} {risk_score:.0f}/100")

st.divider()

# 
============================================================================
# MAIN LAYOUT - Chart + Risk Dashboard
# 
============================================================================
chart_col, risk_col = st.columns([2, 1])

with chart_col:
    st.subheader("📈 Live Market Data")
    
    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(st.session_state.price_history))),
        y=st.session_state.price_history,
        mode='lines',
        name='Underlying',
        line=dict(color='#00d4ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)'
    ))
    
    fig.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, title="Time"),
        yaxis=dict(showgrid=True, gridcolor='#2e3444', title="Price 
($)"),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # P&L chart
    fig_pnl = go.Figure()
    fig_pnl.add_trace(go.Scatter(
        x=list(range(len(st.session_state.pnl_history))),
        y=st.session_state.pnl_history,
        mode='lines',
        name='P&L',
        line=dict(color='#00ff88' if pnl > 0 else '#ff4444', 
width=2),
        fill='tozeroy',
        fillcolor=f'rgba(0, 255, 136, 0.1)' if pnl > 0 else 
'rgba(255, 68, 68, 0.1)'
    ))
    
    fig_pnl.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, title="Time"),
        yaxis=dict(showgrid=True, gridcolor='#2e3444', title="P&L 
($)"),
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_pnl, use_container_width=True)

with risk_col:
    st.subheader("⚠️ Risk Dashboard")
    
    # Greeks display
    def get_risk_color(value, thresholds):
        """Return color based on risk thresholds"""
        abs_val = abs(value)
        if abs_val < thresholds[0]:
            return "#00ff88"
        elif abs_val < thresholds[1]:
            return "#ffaa00"
        else:
            return "#ff4444"
    
    st.markdown("### Portfolio Greeks")
    
    # Delta
    delta_color = get_risk_color(portfolio_greeks['delta'], [500, 
1500])
    st.markdown(f"**Delta:** <span style='color:{delta_color}; 
font-size:24px'>{portfolio_greeks['delta']:.0f}</span>", 
unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['delta']) / 2000))
    
    # Gamma
    gamma_color = get_risk_color(portfolio_greeks['gamma'], [50, 
150])
    st.markdown(f"**Gamma:** <span style='color:{gamma_color}; 
font-size:24px'>{portfolio_greeks['gamma']:.2f}</span>", 
unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['gamma']) / 200))
    
    # Vega
    vega_color = get_risk_color(portfolio_greeks['vega'], [1000, 
3000])
    st.markdown(f"**Vega:** <span style='color:{vega_color}; 
font-size:24px'>{portfolio_greeks['vega']:.0f}</span>", 
unsafe_allow_html=True)
    st.progress(min(1.0, abs(portfolio_greeks['vega']) / 5000))
    
    # Theta
    theta_color = get_risk_color(portfolio_greeks['theta'], [50, 
150])
    st.markdown(f"**Theta:** <span style='color:{theta_color}; 
font-size:24px'>{portfolio_greeks['theta']:.2f}</span>", 
unsafe_allow_html=True)
    
    st.divider()
    
    # Risk warnings
    st.markdown("### Risk Alerts")
    if abs(portfolio_greeks['delta']) > 1500:
        st.error(f"⚠️ High Delta Exposure: 
{portfolio_greeks['delta']:.0f}")
    if abs(portfolio_greeks['gamma']) > 150:
        st.warning(f"⚠️ High Gamma Risk: 
{portfolio_greeks['gamma']:.2f}")
    if len(st.session_state.positions) == 0:
        st.info("✅ No positions - No risk")

st.divider()

# 
============================================================================
# POSITIONS TABLE
# 
============================================================================
st.subheader("📊 Current Positions")

if st.session_state.positions:
    positions_data = []
    for idx, pos in enumerate(st.session_state.positions):
        current_price = black_scholes(
            st.session_state.current_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        
        greeks = calculate_greeks(
            st.session_state.current_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        
        position_pnl = (current_price - pos['purchase_price']) * 
pos['quantity'] * 100 * pos['side']
        
        positions_data.append({
            'ID': idx,
            'Side': 'LONG' if pos['side'] == 1 else 'SHORT',
            'Type': pos['type'].upper(),
            'Strike': f"${pos['strike']:.0f}",
            'Qty': pos['quantity'],
            'Entry': f"${pos['purchase_price']:.2f}",
            'Current': f"${current_price:.2f}",
            'P&L': f"${position_pnl:.0f}",
            'Delta': f"{greeks['delta'] * pos['quantity'] * 100 * 
pos['side']:.0f}",
            'Gamma': f"{greeks['gamma'] * pos['quantity'] * 
100:.2f}",
            'Expiry': pos['expiry_date'].strftime('%Y-%m-%d'),
            'DTE': int(pos['time_to_expiry'] * 365)
        })
    
    df_positions = pd.DataFrame(positions_data)
    st.dataframe(df_positions, use_container_width=True, 
hide_index=True)
    
    # Close position buttons
    close_col1, close_col2 = st.columns([3, 1])
    with close_col1:
        position_to_close = st.selectbox("Select position to close", 
[f"ID {p['ID']} - {p['Type']} {p['Strike']}" for p in 
positions_data])
    with close_col2:
        if st.button("❌ Close Position", type="primary"):
            idx = int(position_to_close.split()[1])
            pos = st.session_state.positions[idx]
            current_price = black_scholes(
                st.session_state.current_price,
                pos['strike'],
                pos['time_to_expiry'],
                0.02,
                0.3,
                pos['type']
            )
            proceeds = current_price * pos['quantity'] * 100 * 
pos['side']
            st.session_state.cash += proceeds
            st.session_state.positions.pop(idx)
            st.success(f"Position closed! Proceeds: 
${proceeds:.0f}")
            st.rerun()
else:
    st.info("No open positions")

# Futures position
st.markdown("### Futures Position")
fut_col1, fut_col2, fut_col3 = st.columns(3)
with fut_col1:
    st.metric("Futures Position", 
f"{st.session_state.futures_position:+.0f} shares")
with fut_col2:
    if 'futures_entry_price' in st.session_state and 
st.session_state.futures_position != 0:
        futures_pnl = (st.session_state.current_price - 
st.session_state.futures_entry_price) * 
st.session_state.futures_position
        st.metric("Futures P&L", f"${futures_pnl:,.0f}")
with fut_col3:
    if st.session_state.futures_position != 0:
        st.metric("Entry Price", 
f"${st.session_state.get('futures_entry_price', 0):.2f}")

st.divider()

# 
============================================================================
# DELTA HEDGING SECTION
# 
============================================================================
st.subheader("🛡️ Delta Hedging (Futures)")

hedge_col1, hedge_col2, hedge_col3 = st.columns([2, 2, 1])

with hedge_col1:
    st.markdown(f"**Current Portfolio Delta:** 
{portfolio_greeks['delta']:.0f}")
    recommended_hedge = -portfolio_greeks['delta']
    st.markdown(f"**Recommended Hedge:** {recommended_hedge:+.0f} 
futures")

with hedge_col2:
    futures_qty = st.number_input(
        "Futures Quantity", 
        min_value=-10000, 
        max_value=10000, 
        value=int(recommended_hedge),
        step=100,
        help="Positive = Long, Negative = Short"
    )
    
    # Transaction cost
    futures_cost = abs(futures_qty) * 0.5  # $0.5 per share
    st.caption(f"Transaction cost: ${futures_cost:.2f}")

with hedge_col3:
    st.write("")  # Spacing
    st.write("")  # Spacing
    if st.button("⚡ Execute Hedge", type="primary"):
        if st.session_state.cash >= futures_cost:
            # Update futures position
            if st.session_state.futures_position == 0 or 
np.sign(futures_qty) == np.sign(st.session_state.futures_position):
                # Opening or adding to position
                total_position = st.session_state.futures_position + 
futures_qty
                if st.session_state.futures_position == 0:
                    st.session_state.futures_entry_price = 
st.session_state.current_price
                else:
                    # Weighted average entry
                    old_notional = st.session_state.futures_position 
* st.session_state.futures_entry_price
                    new_notional = futures_qty * 
st.session_state.current_price
                    st.session_state.futures_entry_price = 
(old_notional + new_notional) / total_position
                st.session_state.futures_position = total_position
            else:
                # Reducing or closing position
                st.session_state.futures_position += futures_qty
                if st.session_state.futures_position == 0:
                    st.session_state.pop('futures_entry_price', 
None)
            
            st.session_state.cash -= futures_cost
            st.success(f"Hedge executed! New position: 
{st.session_state.futures_position:+.0f}")
            st.rerun()
        else:
            st.error("Insufficient cash for transaction cost!")

st.divider()

# 
============================================================================
# CLIENT REQUESTS SECTION (PLACEHOLDER)
# 
============================================================================
st.subheader("📞 Client Requests")
st.info("🔌 **PLACEHOLDER** - Section pour brancher le code de 
génération des requests clients")

# Example of how it could look
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

# 
============================================================================
# CONTROLS
# 
============================================================================
control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    if st.button("⏸️ Pause" if not st.session_state.trading_paused 
else "▶️ Resume", use_container_width=True):
        st.session_state.trading_paused = not 
st.session_state.trading_paused
        st.rerun()

with control_col2:
    if st.button("🔄 Reset Game", use_container_width=True):
        st.session_state.current_price = 100.0
        st.session_state.price_history = [100.0]
        st.session_state.time_history = [datetime.now()]
        st.session_state.cash = 100000.0
        st.session_state.starting_cash = 100000.0
        st.session_state.positions = []
        st.session_state.futures_position = 0
        st.session_state.trade_history = []
        st.session_state.pnl_history = [0]
        st.rerun()

with control_col3:
    if st.button("📜 Trade History", use_container_width=True):
        st.session_state['show_history'] = not 
st.session_state.get('show_history', False)

if st.session_state.get('show_history', False):
    with st.expander("📜 Trade History", expanded=True):
        if st.session_state.trade_history:
            df = pd.DataFrame(st.session_state.trade_history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No trades yet")

# 
============================================================================
# MANUAL TRADING (for testing - can be removed later)
# 
============================================================================
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
            price = black_scholes(st.session_state.current_price, 
strike, days/365, 0.02, 0.3, option_type)
            cost = price * qty * 100
            
            if side == "Long" and st.session_state.cash >= cost:
                st.session_state.cash -= cost
                st.session_state.positions.append({
                    'type': option_type,
                    'strike': strike,
                    'expiry_date': datetime.now() + 
timedelta(days=days),
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
                    'expiry_date': datetime.now() + 
timedelta(days=days),
                    'time_to_expiry': days/365,
                    'quantity': qty,
                    'purchase_price': price,
                    'side': -1
                })
                st.success("Short position opened!")
    import 
streamlit 
as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh

# Page config
st.set_page_config(page_title="Options Trading Game", layout="wide")

# Auto-refresh every 1500ms (1.5 seconds) when not paused
if 'trading_paused' not in st.session_state:
    st.session_state.trading_paused = False

if not st.session_state.trading_paused:
    count = st_autorefresh(interval=1500, key="price_refresh")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_price = 100.0
    st.session_state.price_history = [100.0]
    st.session_state.time_history = [datetime.now()]
    st.session_state.cash = 10000.0
    st.session_state.positions = []
    st.session_state.trade_history = []


# Black-Scholes Option Pricing
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price"""
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
    """Calculate option Greeks"""
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0}

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) / 365

    return {'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega}


def simulate_price_movement(current_price, dt=1 / 252, mu=0.05, sigma=0.3):
    """Simulate price using Geometric Brownian Motion"""
    shock = np.random.normal(0, 1)
    drift = (mu - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * shock
    new_price = current_price * np.exp(drift + diffusion)
    return new_price


# Update price on each refresh (when not paused)
if not st.session_state.trading_paused:
    st.session_state.current_price = simulate_price_movement(st.session_state.current_price)
    st.session_state.price_history.append(st.session_state.current_price)
    st.session_state.time_history.append(datetime.now())

    # Keep only last 100 data points
    if len(st.session_state.price_history) > 100:
        st.session_state.price_history = st.session_state.price_history[-100:]
        st.session_state.time_history = st.session_state.time_history[-100:]

# Header
st.title("📈 Options Trading Game")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Stock Price", f"${st.session_state.current_price:.2f}")
with col2:
    st.metric("Cash", f"${st.session_state.cash:.2f}")
with col3:
    total_portfolio = st.session_state.cash
    for pos in st.session_state.positions:
        option_price = black_scholes(
            st.session_state.current_price,
            pos['strike'],
            pos['time_to_expiry'],
            0.02,
            0.3,
            pos['type']
        )
        total_portfolio += option_price * pos['quantity'] * 100
    st.metric("Portfolio Value", f"${total_portfolio:.2f}")
with col4:
    pnl = total_portfolio - 10000
    st.metric("P&L", f"${pnl:.2f}", delta=f"{(pnl / 10000) * 100:.2f}%")

# Price chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(range(len(st.session_state.price_history))),
    y=st.session_state.price_history,
    mode='lines',
    name='Stock Price',
    line=dict(color='#1f77b4', width=2)
))
fig.update_layout(
    title="Stock Price Movement",
    xaxis_title="Time",
    yaxis_title="Price ($)",
    height=300,
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig, use_container_width=True)

# Trading controls
st.header("Trade Options")

pause_col, reset_col = st.columns([1, 1])
with pause_col:
    if st.button("⏸️ Pause" if not st.session_state.trading_paused else "▶️ Resume"):
        st.session_state.trading_paused = not st.session_state.trading_paused
        st.rerun()

with reset_col:
    if st.button("🔄 Reset Game"):
        st.session_state.current_price = 100.0
        st.session_state.price_history = [100.0]
        st.session_state.time_history = [datetime.now()]
        st.session_state.cash = 10000.0
        st.session_state.positions = []
        st.session_state.trade_history = []
        st.rerun()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Buy Options")
    option_type = st.selectbox("Option Type", ["Call", "Put"])
    strike_price = st.number_input("Strike Price", min_value=50.0, max_value=200.0,
                                   value=float(st.session_state.current_price), step=5.0)
    days_to_expiry = st.slider("Days to Expiry", min_value=1, max_value=90, value=30)
    quantity = st.number_input("Contracts", min_value=1, max_value=100, value=1)

    time_to_expiry = days_to_expiry / 365
    option_price = black_scholes(
        st.session_state.current_price,
        strike_price,
        time_to_expiry,
        0.02,
        0.3,
        option_type.lower()
    )

    greeks = calculate_greeks(
        st.session_state.current_price,
        strike_price,
        time_to_expiry,
        0.02,
        0.3,
        option_type.lower()
    )

    total_cost = option_price * quantity * 100

    st.write(f"**Option Price:** ${option_price:.2f} per share")
    st.write(f"**Total Cost:** ${total_cost:.2f} ({quantity} contract(s) × 100 shares × ${option_price:.2f})")

    with st.expander("📊 Greeks"):
        greek_col1, greek_col2 = st.columns(2)
        with greek_col1:
            st.write(f"**Delta:** {greeks['delta']:.4f}")
            st.write(f"**Gamma:** {greeks['gamma']:.4f}")
        with greek_col2:
            st.write(f"**Theta:** {greeks['theta']:.4f}")
            st.write(f"**Vega:** {greeks['vega']:.4f}")

    if st.button("🛒 Buy Option", type="primary"):
        if st.session_state.cash >= total_cost:
            st.session_state.cash -= total_cost
            st.session_state.positions.append({
                'type': option_type.lower(),
                'strike': strike_price,
                'expiry_date': datetime.now() + timedelta(days=days_to_expiry),
                'time_to_expiry': time_to_expiry,
                'quantity': quantity,
                'purchase_price': option_price,
                'purchase_date': datetime.now()
            })
            st.session_state.trade_history.append({
                'action': 'BUY',
                'type': option_type,
                'strike': strike_price,
                'quantity': quantity,
                'price': option_price,
                'date': datetime.now()
            })
            st.success(f"Bought {quantity} {option_type} option(s)!")
            st.rerun()
        else:
            st.error("Insufficient cash!")

with col2:
    st.subheader("Current Positions")

    if st.session_state.positions:
        for idx, pos in enumerate(st.session_state.positions):
            # Update time to expiry
            time_remaining = (pos['expiry_date'] - datetime.now()).total_seconds() / (365 * 24 * 3600)
            pos['time_to_expiry'] = max(0, time_remaining)

            current_option_price = black_scholes(
                st.session_state.current_price,
                pos['strike'],
                pos['time_to_expiry'],
                0.02,
                0.3,
                pos['type']
            )

            pnl = (current_option_price - pos['purchase_price']) * pos['quantity'] * 100

            with st.container():
                st.write(
                    f"**{pos['type'].upper()} ${pos['strike']:.0f}** | Qty: {pos['quantity']} | Expires: {pos['expiry_date'].strftime('%Y-%m-%d')}")
                st.write(
                    f"Current: ${current_option_price:.2f} | Purchase: ${pos['purchase_price']:.2f} | P&L: ${pnl:.2f}")

                if st.button(f"💰 Sell", key=f"sell_{idx}"):
                    st.session_state.cash += current_option_price * pos['quantity'] * 100
                    st.session_state.trade_history.append({
                        'action': 'SELL',
                        'type': pos['type'].upper(),
                        'strike': pos['strike'],
                        'quantity': pos['quantity'],
                        'price': current_option_price,
                        'date': datetime.now()
                    })
                    st.session_state.positions.pop(idx)
                    st.success(f"Sold for ${current_option_price * pos['quantity'] * 100:.2f}!")
                    st.rerun()

                st.divider()
    else:
        st.info("No open positions")

# Trade history
with st.expander("📜 Trade History"):
    if st.session_state.trade_history:
        df = pd.DataFrame(st.session_state.trade_history)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No trades yet")


print("Hello")
