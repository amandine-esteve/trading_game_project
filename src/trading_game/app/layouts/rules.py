import streamlit as st


def show_rules_page():
    """Display the rules and tutorial page"""
    
    # Header
    st.markdown('<p class="big-title">🎯 FLOW MASTER</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master the Art of Market Making</p>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 👋 Welcome to Flow Master!
        
        You are about to enter the fast-paced world of **market making**. Your goal is to profit from the 
        **bid-ask spread** while managing your inventory risk and adapting to market conditions.
        
        Are you ready to compete against sophisticated trading algorithms?
        """)
    
    # Game Objective
    st.markdown('<p class="section-header">🎯 Game Objective</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Your objective is to **maximize your Profit & Loss (PnL)** by:
    - Quoting competitive **bid** and **ask** prices
    - Earning the **spread** on each completed trade
    - Managing your **inventory** to avoid excessive risk
    - Adapting to changing **market volatility**
    """)
    
    st.markdown('<div class="success-box"><b>Win Condition:</b> Achieve the highest PnL at the end of the trading session while maintaining acceptable risk levels.</div>', unsafe_allow_html=True)
    
    # How to Play
    st.markdown('<p class="section-header">🎮 How to Play</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Quote Your Prices
        - Set your **BID price** (price at which you buy)
        - Set your **ASK price** (price at which you sell)
        - Your spread = Ask - Bid
        
        #### 2️⃣ Trade Execution
        - Market orders arrive randomly
        - **Buy orders** hit your ask (you sell)
        - **Sell orders** hit your bid (you buy)
        - You earn profit from the spread
        """)
    
    with col2:
        st.markdown("""
        #### 3️⃣ Manage Inventory
        - Monitor your position size
        - Positive inventory = you're long (own assets)
        - Negative inventory = you're short (owe assets)
        - Adjust quotes to rebalance
        
        #### 4️⃣ Adapt Strategy
        - Watch market volatility
        - Widen spread in uncertain markets
        - Tighten spread to capture volume
        - React to order flow
        """)
    
    # Market Mechanics
    st.markdown('<p class="section-header">⚙️ Market Mechanics</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Price Discovery
    The market has a **true mid price** that follows a random walk:
    - Base price evolves based on market volatility
    - Your quotes compete with other market makers
    - Best bid and ask determine the market spread
    
    ### Order Flow
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📉 Market Sell Orders**
        - Traders want to sell
        - Hit the highest BID
        - You BUY inventory
        - Position increases
        """)
    
    with col2:
        st.markdown("""
        **📈 Market Buy Orders**
        - Traders want to buy
        - Hit the lowest ASK
        - You SELL inventory
        - Position decreases
        """)
    
    with col3:
        st.markdown("""
        **💰 Your Profit**
        - Captured spread
        - PnL = realized gains
        - Mark-to-market value
        - Total performance
        """)
    
    # Key Concepts
    st.markdown('<p class="section-header">📚 Key Concepts</p>', unsafe_allow_html=True)
    
    with st.expander("💵 Bid-Ask Spread", expanded=False):
        st.markdown("""
        **The spread is your profit margin:**
        - **Bid Price**: Price you pay to BUY
        - **Ask Price**: Price you receive when you SELL
        - **Spread**: Ask - Bid (your potential profit per round trip)
        
        **Example:**
        - You quote Bid: 99.50, Ask: 100.50 (spread = 1.00)
        - Someone sells to you at 99.50 (you buy)
        - Someone buys from you at 100.50 (you sell)
        - **Profit: 1.00 per share**
        
        ⚠️ **Trade-off**: Wider spreads = more profit but fewer trades
        """)
    
    with st.expander("📦 Inventory Management", expanded=False):
        st.markdown("""
        **Your inventory is your risk exposure:**
        - **Long Position** (+): You own assets → exposed to price drops
        - **Short Position** (-): You owe assets → exposed to price rises
        - **Neutral (0)**: No directional risk
        
        **Inventory Skewing:**
        - If long → lower your ask to sell
        - If short → raise your bid to buy
        - Goal: return to neutral position
        
        **Risk:**
        Large inventory × adverse price move = big losses
        """)
    
    with st.expander("📊 Market Volatility", expanded=False):
        st.markdown("""
        **Volatility measures price uncertainty:**
        - **Low Volatility**: Stable prices → tighter spreads possible
        - **High Volatility**: Erratic prices → wider spreads needed
        
        **Adaptation Strategy:**
        - Monitor volatility indicators
        - Widen spread when volatility increases
        - Tighten spread in calm markets
        - Protect against adverse selection
        """)
    
    with st.expander("💸 Profit & Loss (PnL)", expanded=False):
        st.markdown("""
        **Your PnL has multiple components:**
        
        1. **Realized PnL**: 
           - Locked-in profits from completed round trips
           - Cash in your pocket
        
        2. **Unrealized PnL**:
           - Mark-to-market value of current inventory
           - Inventory × (Current Price - Average Entry Price)
        
        3. **Total PnL**: Realized + Unrealized
        
        **Example:**
        - Bought 10 shares at 100
        - Sold 6 shares at 101 → Realized: +6
        - Still hold 4 shares, price now 102 → Unrealized: +8
        - Total PnL: +14
        """)
    
    # Strategy Tips
    st.markdown('<p class="section-header">💡 Strategy Tips</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 For Beginners
        
        **Start Conservative:**
        - Quote near the mid price
        - Use moderate spreads (0.5 - 1.0)
        - Keep inventory small
        - Observe market behavior
        
        **Basic Rules:**
        - ✅ Always quote bid < ask
        - ✅ Stay near mid price
        - ✅ Rebalance inventory often
        - ✅ Widen spread when uncertain
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Advanced Tactics
        
        **Optimize Performance:**
        - Inventory skewing strategies
        - Dynamic spread adjustment
        - Volatility-based pricing
        - Order flow prediction
        
        **Risk Management:**
        - Set position limits
        - Use stop-loss mental levels
        - Diversify across scenarios
        - Monitor competitor quotes
        """)
    
    st.markdown('<div class="warning-box"><b>⚠️ Common Mistakes to Avoid:</b><br>• Quotes too wide → no trades<br>• Quotes too tight → losses from adverse selection<br>• Ignoring inventory → directional risk<br>• Panic adjustments → giving up edge</div>', unsafe_allow_html=True)
    
    # Quick Start
    st.markdown('<p class="section-header">🚀 Quick Start Guide</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Ready to trade? Follow these steps:
    
    1. **🎯 Choose your mode** - Start with Practice Mode if you're new
    2. **⚙️ Configure settings** - Set volatility, game duration, and difficulty
    3. **📊 Review the dashboard** - Familiarize yourself with the interface
    4. **💰 Set your first quotes** - Start conservative: bid/ask near mid price
    5. **👀 Monitor trades** - Watch your PnL and inventory
    6. **🔄 Adapt strategy** - Adjust quotes based on performance
    7. **🏆 Finish strong** - Close positions and maximize final PnL
    """)
    
    st.markdown('<div class="info-box"><b>💡 Pro Tip:</b> Your first few games are for learning. Focus on understanding the mechanics before optimizing for profit.</div>', unsafe_allow_html=True)
    
    # Footer with start button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎮 START TRADING", type="primary", use_container_width=True, key="start_game_btn"):
            st.session_state.show_rules = False
            st.rerun()
    
    st.markdown("<p style='text-align: center; color: #666; margin-top: 20px;'>Good luck, and may the spreads be in your favor! 📈</p>", unsafe_allow_html=True)