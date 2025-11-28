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
<<<<<<< HEAD
        render_single_option_pricing_tab(spot_ref, vol_ref)
=======
        st.subheader("Price a Single Option")

        # ---------- OPTION TYPE ----------
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Option Type</span>",
            unsafe_allow_html=True
        )
        pricer_opt_type = st.selectbox(
            "pricer_opt_type",
            ["call", "put"],
            key="pricer_opt_type",
            label_visibility="collapsed"
        )

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
            st.markdown(
                "<br><span style='color:white; font-weight:bold;'>Results</span>",
                unsafe_allow_html=True
            )

            pricer_option = Option(
                K=pricer_strike,
                T=pricer_maturity/ BASE,
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
>>>>>>> 9126b14 (clean up and comment)

    # ============================================================================
    # TAB 2: STRATEGY PRICER
    # ============================================================================
    with pricer_tab2:
<<<<<<< HEAD
        render_vanilla_strategy_pricing_tab(spot_ref, vol_ref)
    st.divider()
=======
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

        strat_spot = float(st.session_state.stock.last_price)
        strat_rf = RF

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
                t_short = strat_short_days / BASE
                t_long = strat_long_days / BASE
            else:
                st.markdown(
                    "<span style='color:white;'>Days to Expiry</span>",
                    unsafe_allow_html=True
                )
                strat_maturity_days = st.slider(
                    "strat_mat_days",
                    min_value=1,
                    max_value=BASE,
                    value=30,
                    key="strat_pricer_dte",
                    label_visibility="collapsed"
                )
                strat_maturity = strat_maturity_days / BASE

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
                    value=float(strat_spot - 0.05*strat_spot),
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
                    value=float(strat_spot + 0.05*strat_spot),
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
                    value=float(strat_spot - 0.10*strat_spot),
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
                    value=float(strat_spot + 0.10 * strat_spot),
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
>>>>>>> 9126b14 (clean up and comment)
