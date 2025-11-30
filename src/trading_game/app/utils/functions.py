# import streamlit as st
#
# import numpy as np
# from scipy.stats import norm
# from trading_game.core.book import Book
#
# def calculate_risk_score(book: Book):
#     """Risk score based on delta, gamma, and P&L"""
#     greeks = book.compute_greeks(st.session_state.stock.last_price, st.session_state.stock.last_vol)
#     portfolio_value = book.compute_book_value(st.session_state.stock.last_price, st.session_state.stock.last_vol)
#
#     delta_risk = abs(greeks['delta']) / 1000
#     gamma_risk = abs(greeks['gamma']) / 100
#
#     pnl = portfolio_value - st.session_state.starting_cash
#     pnl_score = max(0, pnl / st.session_state.starting_cash * 100)
#
#     score = max(0, 100 - delta_risk * 30 - gamma_risk * 20 + pnl_score * 50)
#
#     return min(100, score)