import pandas as pd
import streamlit as st

from trading_game.app.utils.functions import black_scholes, calculate_greeks



def render_current_positions() -> None:
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