import streamlit as st

from trading_game.app.components.graphs import render_stock_chart, render_pnl_chart
from trading_game.app.components.news_alert import render_news
from trading_game.app.components.risk_bar import render_risk_bar
from trading_game.app.utils.styling import get_risk_color

def render_market_overview(pnl, portfolio_greeks) -> None :
    st.markdown('<a id="market-overview"></a>', unsafe_allow_html=True)
    st.header("📊 Market Overview")

    render_news()

    chart_col, risk_col = st.columns([2, 1])
    with chart_col:
        x_values = list(range(len(st.session_state.stock.price_history)))

        st.subheader(f"📈 Live Price - {st.session_state.stock.name} {st.session_state.stock.ticker}")
        render_stock_chart(x_values)

        # === P&L Evolution ===
        st.subheader("💰 P&L Evolution")
        render_pnl_chart(x_values, pnl)

    with risk_col:
        st.markdown('<a id="risk-dashboard"></a>', unsafe_allow_html=True)
        st.subheader("⚠️ Risk Dashboard")

        st.markdown("#### Portfolio Greeks")

        delta_color = get_risk_color(portfolio_greeks['delta'], [500, 1500])
        gamma_color = get_risk_color(portfolio_greeks['gamma'], [50, 150])
        vega_color = get_risk_color(portfolio_greeks['vega'], [1000, 3000])
        theta_color = get_risk_color(portfolio_greeks['theta'], [50, 150])

        st.markdown(
            f"**Delta:** <span style='color:{delta_color}; font-size:24px'>{portfolio_greeks['delta']:.0f}</span>",
            unsafe_allow_html=True)
        render_risk_bar(portfolio_greeks['delta'], 2000)
        st.markdown(
            f"**Gamma:** <span style='color:{gamma_color}; font-size:24px'>{portfolio_greeks['gamma']:.2f}</span>",
            unsafe_allow_html=True)
        render_risk_bar(portfolio_greeks['gamma'], 200)
        st.markdown(f"**Vega:** <span style='color:{vega_color}; font-size:24px'>{portfolio_greeks['vega']:.0f}</span>",
                    unsafe_allow_html=True)
        render_risk_bar(portfolio_greeks['vega'], 5000)
        st.markdown(
            f"**Theta:** <span style='color:{theta_color}; font-size:24px'>{portfolio_greeks['theta']:.2f}</span>",
            unsafe_allow_html=True)
        render_risk_bar(portfolio_greeks['theta'], 150)

        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.markdown("#### Risk Alerts")
        if abs(portfolio_greeks['delta']) > 1500:
            st.error(f"⚠️ High Delta Exposure: {portfolio_greeks['delta']:.0f}")
        if abs(portfolio_greeks['gamma']) > 150:
            st.warning(f"⚠️ High Gamma Risk: {portfolio_greeks['gamma']:.2f}")
        if len(st.session_state.positions) == 0:
            st.info("✅ No positions - No risk")

    st.divider()