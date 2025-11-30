import streamlit as st

from trading_game.app.components.pricer_tabs import render_single_option_pricing_tab, render_vanilla_strategy_pricing_tab

def render_pricer_tool() -> None:
    st.markdown('<a id="pricer"></a>', unsafe_allow_html=True)
    st.header("🧮 Options Pricer Tool")

    pricer_tab1, pricer_tab2 = st.tabs(["Vanilla Options", "Strategies"])

    spot_ref = st.session_state.stock.last_price
    vol_ref = st.session_state.stock.last_vol

    # ============================================================================
    # TAB 1: SINGLE OPTION PRICER
    # ============================================================================
    with pricer_tab1:
        render_single_option_pricing_tab(spot_ref, vol_ref)

    # ============================================================================
    # TAB 2: STRATEGY PRICER
    # ============================================================================
    with pricer_tab2:
        render_vanilla_strategy_pricing_tab(spot_ref, vol_ref)
    st.divider()
