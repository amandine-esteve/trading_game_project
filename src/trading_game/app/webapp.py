import random
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh

from trading_game.config.settings import REFRESH_INTERVAL
from trading_game.utils.app_utils import create_stock, create_street
from trading_game.core.street import QuoteRequest
from trading_game.core.book import Book
from trading_game.core.option_pricer import Strategy, Greeks

from trading_game.core.manual_trading import (
    OrderExecutor, VanillaOrder, StrategyOrder,
    OrderSide, OrderType, StrategyType, OrderStatus
)
from trading_game.core.option_pricer import Option, Strategy

# ============================================================================
# PAGE CONFIG - Dark Theme
# ============================================================================
st.set_page_config(
    page_title="Options Market Maker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remove Streamlit default top padding and toolbar
st.markdown("""
    <style>
        /* Supprimer la barre blanche supérieure et le menu Streamlit */
        header {visibility: hidden;}
        /* Supprime la marge du haut du conteneur principal */
        .block-container {
            padding-top: 0rem !important;
        }
        /* Si une bande blanche subsiste, forcer un fond sombre */
        body {
            background-color: #0e1117;
        }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for dark theme
st.markdown("""
<style>
/* ---------- App Background & Global Text ---------- */
.stApp {
    background-color: #0e1117;
    color: #ffffff !important;
}

/* ---------- Sidebar Header Background ---------- */
[data-testid="stSidebarHeader"] {
    background-color: #0e1117 !important;
}

/* ---------- Sidebar Background ---------- */

[data-testid="stSidebar"] {
    background-color: #0e1117 !important;
}

/* ---------- Sidebar Navigation Title ---------- */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* ---------- Sidebar / Navigation Links ---------- */
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

/* ---------- Metric Cards ---------- */
.metric-card {
    background-color: #1e2130;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #2e3444;
}

div[data-testid="stMetricLabel"] {
    color: white !important;
}
div[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: bold;
    font-size: 28px;
}
div[data-testid="stMetricDelta"] {
    color: white !important;
}
            
[data-testid="stMetricLabel"], 
[data-testid="stMetricValue"], 
[data-testid="stMetricDelta"] {
    color: #ffffff !important;
    text-shadow: none !important;
}

/* ---------- Risk Coloring ---------- */
.risk-high { color: #ff4444 !important; font-weight: bold; }
.risk-medium { color: #ffaa00 !important; }
.risk-low { color: #00ff88 !important; }

/* ---------- Buttons ---------- */
.stButton>button {
    background-color: #ff4444 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 5px;
}
.stButton>button:hover {
    background-color: #ff6666 !important;
}

.stButton.secondary>button {
    background-color: #1e2130 !important;
    color: white !important;
}

/* ---------- Sliders, selects, inputs ---------- */
.stSlider, .stSelectbox, .stNumberInput, .stRadio {
    color: #ffffff !important;
}

/* ---------- Checkbox ---------- */
[data-baseweb="checkbox"] input:checked + div {
    background-color: #ff4444 !important;
}
[data-baseweb="checkbox"] label {
    color: white !important;
}

/* ---------- Progress Bars ---------- */
.stProgress>div>div>div>div {
    background-color: #ff4444 !important;
}
.stProgress>div>div>div {
    background-color: #1e2130 !important;
    color: white !important;
}

/* ---------- Expanders ---------- */
.stExpander {
    background-color: #1e2130 !important;
    color: white !important;
}
.stExpander .stMarkdown,
.stExpander .stDataFrame,
.stExpander .stText {
    color: white !important;
}
div[data-testid="stDataFrameContainer"] {
    color: white !important;
    background-color: #0e1117 !important;
}
div[data-testid="stInfo"] {
    color: white !important;
    background-color: #1e2130 !important;
    border: 1px solid #2e3444;
}

/* ---------- Headers / Labels / Static text ---------- */
.css-1v3fvcr, .css-1kyxreq, .css-1q8dd3e {
    color: #ffffff !important;
}

/* ---------- Risk Bars (Delta, Gamma, Vega, Theta) ---------- */
.risk-bar-container {
    position: relative;
    width: 100%;
    height: 16px;
    background-color: #2e3444;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 8px;
}
.risk-bar {
    height: 100%;
    position: absolute;
    top: 0;
}

/* ---------- Tabs: Style général ---------- */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1e2130 !important;
    gap: 5px;
    padding: 5px;
    border-radius: 8px;
}

/* Tabs non sélectionnées */
.stTabs [data-baseweb="tab-list"] button {
    background-color: #2e3444 !important;
    color: #ffffff !important;
    border-radius: 5px;
    padding: 10px 20px;
    font-weight: 500;
    border: none;
}

/* Tabs au hover */
.stTabs [data-baseweb="tab-list"] button:hover {
    background-color: #3e4454 !important;
    color: #ffffff !important;
}

/* Tab sélectionnée */
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #ff4444 !important;
    color: #ffffff !important;
    font-weight: bold;
    border-bottom: 3px solid #ff6666;
}

/* Texte dans les tabs */
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-size: 16px;
    margin: 0;
}

/* Contenu des tabs */
.stTabs [data-baseweb="tab-panel"] {
    background-color: #1e2130 !important;
    padding: 20px;
    border-radius: 8px;
    margin-top: 10px;
}

/* ---------- Labels des inputs ---------- */
label[data-testid="stWidgetLabel"] {
    color: #ffffff !important;
    font-weight: 500;
}

/* ---------- Radio buttons ---------- */
/* Texte des boutons */
/* Texte des boutons non sélectionnés */
.stRadio > label {
    color: #ffffff !important;  /* texte blanc */
    font-weight: normal;
}

/* Fond neutre des boutons (non sélectionnés) */
.stRadio [data-baseweb="radio"] > div {
    background-color: #2e3444;  /* fond sombre */
    border-radius: 8px;
    padding: 5px 0;  /* padding vertical uniquement */
    margin-right: 8px;
    display: flex;
    align-items: center;
    gap: 5px;  /* espace entre cercle et texte */
    border: 1px solid #444c5c;
    color: #ffffff !important;  /* texte blanc */
}

/* Bouton sélectionné : fond rouge derrière cercle + texte */
.stRadio [data-baseweb="radio"] input:checked + div {
    background-color: #ff4444 !important;  /* rouge vif */
    color: #ffffff !important;  /* texte blanc sur fond rouge */
    border: 1px solid #ff4444 !important;
    font-weight: bold;
    padding-left: 5px;  /* ajuste cercle */
    padding-right: 5px; /* ajuste texte */
}


/* ---------- Selectbox ---------- */
[data-baseweb="select"] {
    color: #ffffff !important;
}

[data-baseweb="select"] > div {
    background-color: #1e2130 !important;
    color: #ffffff !important;
    border-color: #2e3444 !important;
}

/* ---------- Input Text Color ---------- */
[data-baseweb="input"] input {
    color: #0e1117 !important;
}

/* Number input text */
[data-baseweb="base-input"] input {
    color: #0e1117 !important;
}

/* Text input */
input[type="text"],
input[type="number"] {
    color: #0e1117 !important;
}

/* Textarea */
textarea {
    color: #0e1117  git  !important;
}

/* ---------- Slider ---------- */
[data-baseweb="slider"] {
    color: #ffffff !important;
}

[data-baseweb="slider"] [role="slider"] {
    background-color: #ff4444 !important;
}

/* ---------- Expander header + visible ---------- */
.streamlit-expanderHeader {
    background-color: #1e2130 !important;
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 1px solid #2e3444;
    border-radius: 5px;
}

.streamlit-expanderHeader:hover {
    background-color: #2e3444 !important;
}

/* ---------- Success/Error messages ---------- */
.stSuccess {
    background-color: #0e7a0e !important;
    color: #ffffff !important;
    border: 1px solid #00ff88 !important;
}

.stError {
    background-color: #a51c30 !important;
    color: #ffffff !important;
    border: 1px solid #ff4444 !important;
}

.stInfo {
    background-color: #1e3a5f !important;
    color: #ffffff !important;
    border: 1px solid #4a90e2 !important;
}

/* ---------- Markdown headings dans manual trading ---------- */
.stMarkdown h4, .stMarkdown h3, .stMarkdown h2 {
    color: #ffffff !important;
    font-weight: bold;
}

.stMarkdown p {
    color: #ffffff !important;
}

/* ---------- Divider + visible ---------- */
hr {
    border-color: #2e3444 !important;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE FIRST (before auto-refresh!)
# ============================================================================

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.stock = create_stock()
    st.session_state.street = create_street()
    st.session_state.book = Book()
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

# Intialize Order Executor
if 'order_executor' not in st.session_state:
    st.session_state.order_executor = OrderExecutor(max_position_size=1000)

# ============================================================================
# PRICING FUNCTIONS 
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
    """Calculate Greeks """
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
        # Cas 1 : vanilla option avec une seule strike
        if 'strike' in pos:
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

        # Cas 2 : structure à + d'1 strike (ex: call spread)
        elif 'strikes' in pos:
            strikes = pos['strikes']
            weights = pos.get('weights', [1/len(strikes)] * len(strikes))  # pondération éventuelle
            for strike, weight in zip(strikes, weights):
                greeks = calculate_greeks(
                    st.session_state.stock.last_price,
                    strike,
                    pos['time_to_expiry'],
                    0.02,
                    0.3,
                    pos['type']
                )

                multiplier = pos['quantity'] * 100 * pos['side'] * weight
                total_delta += greeks['delta'] * multiplier
                total_gamma += greeks['gamma'] * multiplier
                total_vega += greeks['vega'] * multiplier
                total_theta += greeks['theta'] * multiplier

        else:
            print(f"⚠️ Position without strike(s): {pos}")

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
        try:
            # Vérifier si c'est une position vanilla (avec 'strike') ou strategy (avec 'strikes')
            if 'strike' in pos and isinstance(pos.get('strike'), (int, float)):
                # Position vanilla (Call ou Put simple)
                option_price = black_scholes(
                    st.session_state.stock.last_price,
                    pos['strike'],
                    pos['time_to_expiry'],
                    0.02,
                    0.3,
                    pos['type']
                )
                total += option_price * pos['quantity'] * 100 * pos['side']
            
            elif 'strikes' in pos:
                # Position strategy (Spread, Straddle, Strangle)
                from trading_game.core.option_pricer import Strategy
                
                strat_type = pos['type'].lower()
                
                # Recalculer le prix de la stratégie
                if 'call spread' in strat_type or 'call_spread' in strat_type:
                    strat = Strategy.call_spread(
                        k1=pos['strikes'][0],
                        k2=pos['strikes'][1],
                        t=pos['time_to_expiry'],
                        r=0.02
                    )
                elif 'put spread' in strat_type or 'put_spread' in strat_type:
                    strat = Strategy.put_spread(
                        k1=pos['strikes'][0],
                        k2=pos['strikes'][1],
                        t=pos['time_to_expiry'],
                        r=0.02
                    )
                elif 'straddle' in strat_type:
                    strat = Strategy.straddle(
                        k=pos['strikes'][0],
                        t=pos['time_to_expiry'],
                        r=0.02
                    )
                elif 'strangle' in strat_type:
                    strat = Strategy.strangle(
                        k1=pos['strikes'][0],
                        k2=pos['strikes'][1],
                        t=pos['time_to_expiry'],
                        r=0.02
                    )
                else:
                    # Si type inconnu, skip cette position
                    continue
                
                strategy_price = strat.price(S=st.session_state.stock.last_price, sigma=0.3)
                total += strategy_price * pos['quantity'] * 100 * pos['side']
        
        except Exception as e:
            # En cas d'erreur, on continue avec les autres positions
            st.warning(f"⚠️ Error calculating position: {e}")
            continue

    # Futures P&L 
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

    st.sidebar.markdown("""
    <a href="#market-overview" class="nav-link">📊 Market Overview</a>
    <a href="#risk-dashboard" class="nav-link">⚠️ Risk Dashboard</a>
    <a href="#positions" class="nav-link">📈 Positions</a>
    <a href="#hedging" class="nav-link">🛡️ Delta Hedging</a>
    <a href="#clients" class="nav-link">📞 Client Requests</a>
    <a href="#manual-trading" class="nav-link">💼 Manual Trading</a>
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
    score_color = "🟢" if risk_score > 80 else "🟡" if risk_score > 40 else "🔴"
    st.metric("Risk Score", f"{score_color} {risk_score:.0f}/100")

st.divider()


def render_risk_bar(value, max_abs):
    """
    Render a horizontal bar where negative values fill to the left in red,
    positive values fill to the right in blue.
    max_abs is the maximum absolute value for scaling.
    """
    # Clamp value to [-max_abs, max_abs]
    value = max(-max_abs, min(max_abs, value))
    # Calculate percentage
    pct = abs(value) / max_abs * 50  # 50% is half of the bar
    color = "#00aaff" if value >= 0 else "#ff4444"
    direction = "left" if value >= 0 else "right"

    html = f"""
    <div style="position: relative; width: 100%; height: 20px; background-color: #2e3444; border-radius: 10px;">
        <div style="
            position: absolute;
            {direction}: 50%;
            width: {pct}%;
            height: 100%;
            background-color: {color};
            border-radius: 8px;
        "></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

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
    y_values = st.session_state.stock.price_history

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
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

    # === Dynamically set y-axis range to give visual breathing room ===
    y_min = min(y_values)
    y_max = max(y_values)
    y_range = y_max - y_min if y_max != y_min else 1
    padding = y_range * 0.3  # 30% padding top/bottom for better centering

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
            range=[y_min - padding, y_max + padding],
            zeroline=False
        ),
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # === P&L Evolution ===
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

    st.markdown("### Portfolio Greeks")

    def get_risk_color(value, thresholds):
        abs_val = abs(value)
        if abs_val < thresholds[0]:
            return "#00ff88"
        elif abs_val < thresholds[1]:
            return "#ffaa00"
        else:
            return "#ff4444"

    delta_color = get_risk_color(portfolio_greeks['delta'], [500, 1500])
    gamma_color = get_risk_color(portfolio_greeks['gamma'], [50, 150])
    vega_color = get_risk_color(portfolio_greeks['vega'], [1000, 3000])
    theta_color = get_risk_color(portfolio_greeks['theta'], [50, 150])

    st.markdown(f"**Delta:** <span style='color:{delta_color}; font-size:24px'>{portfolio_greeks['delta']:.0f}</span>", unsafe_allow_html=True)
    render_risk_bar(portfolio_greeks['delta'], 2000)
    st.markdown(f"**Gamma:** <span style='color:{gamma_color}; font-size:24px'>{portfolio_greeks['gamma']:.2f}</span>", unsafe_allow_html=True)
    render_risk_bar(portfolio_greeks['gamma'], 200)
    st.markdown(f"**Vega:** <span style='color:{vega_color}; font-size:24px'>{portfolio_greeks['vega']:.0f}</span>", unsafe_allow_html=True)
    render_risk_bar(portfolio_greeks['vega'], 5000)
    st.markdown(f"**Theta:** <span style='color:{theta_color}; font-size:24px'>{portfolio_greeks['theta']:.2f}</span>", unsafe_allow_html=True)
    render_risk_bar(portfolio_greeks['theta'], 150)

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

st.markdown("### Position")
fut_col1, fut_col2, fut_col3 = st.columns(3)
with fut_col1:
    st.metric("Position", f"{st.session_state.futures_position:+.0f} shares")
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
st.header("🛡️ Delta Hedging")

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

            # ADD TRADE TO BOOK
            trade_id = st.session_state.book.add_trade_stock(
            st.session_state.stock,
            futures_qty,
            st.session_state.stock.last_price,
            st.session_state.stock.vol)   

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
            st.session_state.stock.vol)  # check if right spot ref

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
            if msg['type'] == 'request' or msg['type']=='market_response':
                # Quote request from market
                st.markdown(f"""
                <div style="background-color: #d0d4db; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%;">
                    <small style="color: #666;">{msg['timestamp']}</small><br>
                    <strong>Trader:</strong> {msg['message']}
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
                    result = st.session_state.quote_request.evaluate_bid_ask(bid_price, ask_price, st.session_state.stock.last_price, st.session_state.stock.vol)
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
st.header("💼 Manual Trading")
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
            maturity=days/365,
            spot_price=st.session_state.stock.last_price,
            volatility=st.session_state.stock.vol,
            risk_free_rate=0.05,
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
                    'time_to_expiry': days/365,
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
        "Strategy Type", ["Call Spread", "Put Spread", "Straddle", "Strangle"], key="strat_type"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        side_strat = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="strat_side")
        
        if strat_type in ["Call Spread", "Put Spread", "Strangle"]:
            strike1 = st.number_input(
                "Strike 1", value=float(st.session_state.stock.last_price - 5), step=5.0, key="strat_k1"
            )
            strike2 = st.number_input(
                "Strike 2", value=float(st.session_state.stock.last_price + 5), step=5.0, key="strat_k2"
            )
            strikes = [strike1, strike2]
        else:  # Straddle
            strike_atm = st.number_input(
                "Strike (ATM)", value=float(st.session_state.stock.last_price), step=5.0, key="strat_k"
            )
            strikes = [strike_atm]
    
    with col2:
        days_strat = st.slider("Days to Expiry", 1, 365, 30, key="strat_dte")
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
            "Strangle": StrategyType.STRANGLE
        }
        
        strategy_order = StrategyOrder(
            side=OrderSide.BUY if side_strat == "Buy" else OrderSide.SELL,
            order_type=OrderType.MARKET if order_type_strat == "Market" else OrderType.LIMIT,
            quantity=qty_strat,
            strategy_type=strat_type_map[strat_type],
            strikes=strikes,
            maturity=days_strat/365,
            spot_price=st.session_state.stock.last_price,
            volatility=st.session_state.stock.vol,
            risk_free_rate=0.05,
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
                    'time_to_expiry': days_strat/365,
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
    if st.button("⏸️ Pause" if not st.session_state.trading_paused else "▶️ Resume", use_container_width=True, type="primary"):
        st.session_state.trading_paused = not st.session_state.trading_paused
        st.rerun()

with control_col2:
    if st.button("🔄 Reset Game", use_container_width=True, type= "primary"):
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