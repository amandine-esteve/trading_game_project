import streamlit as st

import numpy as np
from scipy.stats import norm

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
        futures_pnl = (
                                  st.session_state.stock.last_price - st.session_state.futures_entry_price) * st.session_state.futures_position
        total += futures_pnl

    return total

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