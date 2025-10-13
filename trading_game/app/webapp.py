import streamlit as st
import numpy as np
import pandas as pd
import random



# ----- PARAMETERS -----
np.random.seed(42)
random.seed(42)

T = 100 # number of steps
initial_price = 100.0
initial_cash = 100000
mu = 0.0005
sigma = 0.01
news_prob = 0.15

# ----- SESSION STATE -----
if "t" not in st.session_state:
    st.session_state.t = 0
    st.session_state.price = initial_price
    st.session_state.cash = initial_cash
    st.session_state.position = 0
    st.session_state.history = []
    st.session_state.news = []

# ----- FUNCTIONS -----
def generate_news(t):
    if random.random() < news_prob:
        polarity = random.choice(["positive", "negative"])
        impact = np.random.uniform(0.5, 2.0)
        return {"time": t, "polarity": polarity, "impact": impact,
                "headline": f"{polarity.title()} news at t={t}"}
    return None

def simulate_price(prev_price, news):
    drift = mu * prev_price
    shock = sigma * prev_price * np.random.randn()
    price = prev_price + drift + shock
    if news:
        jump = (news["impact"]/100.0) * prev_price
        price += jump if news["polarity"] == "positive" else -jump
    return max(price, 0.01)

# ----- UI -----
st.title("📈 Asset Manager Trading Game")

if st.session_state.t < T:
    # Generate news
    news = generate_news(st.session_state.t)
    new_price = simulate_price(st.session_state.price, news)

if news:
    st.warning(f"📰 News: {news['headline']} (impact {news['impact']:.2f}%)")

    st.write(f"**Time step:** {st.session_state.t}")
    st.write(f"**Current Price:** {new_price:.2f}")
    st.write(f"**Cash:** {st.session_state.cash:.2f}")
    st.write(f"**Position:** {st.session_state.position} shares")
    st.write(f"**Portfolio Value:** {st.session_state.cash + st.session_state.position * new_price:.2f}")

# Player actions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("BUY 10"):
        cost = 10 * new_price
        if st.session_state.cash >= cost:
            st.session_state.cash -= cost
            st.session_state.position += 10
with col2:
    if st.button("SELL 10"):
        qty = min(10, st.session_state.position)
        st.session_state.cash += qty * new_price
        st.session_state.position -= qty
with col3:
    if st.button("HOLD"):
        pass

# Save history
portfolio_value = st.session_state.cash + st.session_state.position * new_price
st.session_state.history.append({
"time": st.session_state.t,
"price": new_price,
"cash": st.session_state.cash,
"position": st.session_state.position,
"portfolio_value": portfolio_value
})
if news:
    st.session_state.news.append(news)

# Update step
st.session_state.price = new_price
st.session_state.t += 1

# Plot charts
if len(st.session_state.history) > 1:
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df.set_index("time")[["price", "portfolio_value"]])
else:
    st.success("✅ Game Over! Here are your results:")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df.tail())

# Metrics
total_return = df["portfolio_value"].iloc[-1] / df["portfolio_value"].iloc[0] - 1
st.metric("Final Portfolio Value", f"{df['portfolio_value'].iloc[-1]:.2f}")
st.metric("Total Return", f"{total_return*100:.2f}%")
st.line_chart(df.set_index("time")[["price", "portfolio_value"]])


