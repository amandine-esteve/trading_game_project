import streamlit as st

from trading_game.app.layouts.client_requests import render_client_requests
from trading_game.app.layouts.controls import render_controls
from trading_game.app.layouts.current_positions import render_current_positions
from trading_game.app.layouts.market_overview import render_market_overview
from trading_game.app.layouts.pricer_tool import render_pricer_tool
from trading_game.app.layouts.trading_delta import render_trading_delta
from trading_game.app.layouts.trading_options import render_trading_options
from trading_game.app.components.metrics import render_top_metrics
from trading_game.app.components.sidebar_header import render_header, render_side_bar
from trading_game.app.utils.styling import remove_st_default, global_theme



def render_main_layout() -> None:
    # Styling
    remove_st_default()
    global_theme()

    # First computations -> check recomputation
    spot_ref = st.session_state.stock.last_price
    vol_ref = st.session_state.stock.last_vol
    book = st.session_state.book
    cash_available = book.cash
    total_portfolio_value = book.compute_book_value(spot_ref, vol_ref)
    portfolio_pnl = book.compute_book_pnl(spot_ref, vol_ref)
    portfolio_greeks = book.compute_greeks(spot_ref, vol_ref)
    score = 0  # calculate_risk_score(book) # implement scoring method

    # BAR AND HEADER
    render_side_bar()
    render_header(portfolio_pnl, score)

    # METRICS
    render_top_metrics(total_portfolio_value, portfolio_pnl, score, cash_available)

    # ============================================================================
    # MARKET OVERVIEW
    # ============================================================================
    render_market_overview(portfolio_pnl, portfolio_greeks)

    # ============================================================================
    # POSITIONS TABLE
    # ============================================================================
    render_current_positions()

    # ============================================================================
    # DELTA
    # ============================================================================
    render_trading_delta(portfolio_greeks, cash_available)

    # ============================================================================
    # CLIENT REQUESTS
    # ============================================================================
    render_client_requests()

    # ============================================================================
    # MANUAL TRADING -> refactor
    # ============================================================================
    render_trading_options()

    # ============================================================================
    # PRICER TOOL
    # ============================================================================
    render_pricer_tool()

    # ============================================================================
    # CONTROLS
    # ============================================================================
    render_controls()
