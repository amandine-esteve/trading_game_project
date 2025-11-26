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
from trading_game.app.utils.functions import *



def render_main_layout() -> None:
    # Styling
    remove_st_default()
    global_theme()

    # BAR AND HEADER
    render_side_bar()
    render_header()

    # First computations -> to update with Book methods
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
    # POSITIONS TABLE -> refactor
    # ============================================================================
    render_current_positions()

    # ============================================================================
    # DELTA -> refactor
    # ============================================================================
    render_trading_delta(portfolio_greeks)

    # ============================================================================
    # CLIENT REQUESTS
    # ============================================================================
    render_client_requests()

    # ============================================================================
    # MANUAL TRADING -> refactor
    # ============================================================================
    render_trading_options()

    # ============================================================================
    # PRICER TOOL -> refactor
    # ============================================================================
    render_pricer_tool()

    # ============================================================================
    # CONTROLS
    # ============================================================================
    render_controls()
