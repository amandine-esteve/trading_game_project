import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh

import sys
sys.path.extend(['C:\\Users\\amand\\Desktop\\M2\\python\\trading_game_project'])

from settings import REFRESH_INTERVAL
from src.trading_game.core.market import Stock



# Page config
st.set_page_config(page_title="Flow Master", layout="wide")

# Auto-refresh every 1500ms (1.5 seconds) when not paused
if 'trading_paused' not in st.session_state:
    st.session_state.trading_paused = False

if not st.session_state.trading_paused:
    count = st_autorefresh(interval=REFRESH_INTERVAL, key="price_refresh")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    #stock = Stock(name="ABC", ticker="ABC", sector="tech", rate=0.05, vol = 0.20, init_price=100)
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