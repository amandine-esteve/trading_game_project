import streamlit as st
from pathlib import Path
import pandas as pd

def show_rules_page() -> None:
    """Display the rules and tutorial page for the options market making game"""
   
    col1, col2 = st.columns([0.5, 5])

    with col1:
        # Use absolute path to avoid issues with working directory
        logo_path = Path(__file__).parent.parent / "images" / "logo_vf.jpeg"
        st.image(str(logo_path), width=80)

    with col2:
        st.markdown("""
        <h1 style='margin-top: -10px;'>Flow Master Dashboard</h1>
        """, unsafe_allow_html=True)

    # Introduction
    st.markdown("---")
    st.markdown("""
    ### 👋 Welcome to Flow Master!

    You are an **options market maker** at a trading desk. Your role is to provide liquidity to the market 
    by quoting **bid-ask prices** on vanilla options and strategies to a diverse panel of clients: such as hedge funds, 
    asset managers, investment banks...

    Your mission: **maximize your P&L** while managing your **Greeks exposure**.

    Are you ready to compete in the options trading arena?
    """)
    st.markdown("---")

    # Game Objective
    st.markdown('<p class="section-header">🎯 Game Objective</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Your objective is to **maximize your Profit & Loss (P&L)** by:
    - **Quoting competitive prices** to client requests (calls, puts, strategies)
    - **Capturing the bid-ask spread** on every trade
    - **Managing your Greeks** (Delta, Gamma, Vega, Theta) to control risk
    - **Hedging your Delta** using the underlying stock
    - **Adjusting your volatility correctly** to avoid being arbitraged
    """)
    
    st.markdown('<div class="success-box"><b>🏆 Win Condition:</b> Achieve the highest P&L at game end while keeping your Greeks under control.</div>', unsafe_allow_html=True)
    st.markdown("---")

    # How to Play - Step by Step
    st.markdown('<p class="section-header">🎮 How to Play: Step-by-Step</p>', unsafe_allow_html=True)

    # Steps 1 & 2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📞 Step 1: Receive Client Quote Requests
        
        Client requests appear in the **"Client Requests"** panel. Each request includes:
        - **Client name** (Hedge Fund, Asset Manager, Investment Bank)
        - **Option type** (Call or Put) or **Strategy** (Straddle, Strangle, etc.)
        - **Strike price** (K)
        - **Maturity** (1M, 3M, 6M, etc.)
        - **Quantity** (The notional amount)
        
        Your job is to **quote a bid and ask price** to this client.
        """)

    with col2:
        st.markdown("""
        ### 🧮 Step 2: Price the Option Using the Pricer
        
        Use the **"Options Pricer Tool"** to calculate the fair value:

        1. **Select the option type** (Call/Put or Strategy)
        2. **Match the maturity** from the client request (1M, 3M, ...) and the **strike** provided.
        3. **🔑 Adjust the volatility (σ) if you want**. By default the pricer gives you the stock's **implied volatility**, 
        but you can modify it to express your pricing view:
        - Higher vol → higher option price
        - Lower vol → lower option price
        4. **Press Enter** to compute the price and Greeks

        The pricer will display:
        - The **Option (or strategy) fair value**
        - The corresponding **Greeks**: Delta, Gamma, …
        """)

    st.markdown(
        '<div class="warning-box">'
        '<b>⚠️ Critical:</b> The pricer gives you the stock’s implied volatility by default, '
        'but adjusting it is a lever you control to influence your pricing and edges.'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")

    # Steps 3 & 4
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 💰 Step 3: Quote Your Bid-Ask Spread
        
        Now enter your **bid and ask prices** in the **"Trading Options"** panel:
        
        - **Bid price** (what you'll pay to BUY from the client)
        - **Ask price** (what you'll charge to SELL to the client)
        
        **Strategy considerations:**
        - **Aggressive quoting**: Tight spread → more trades, less profit per trade
        - **Conservative quoting**: Wide spread → fewer trades, more profit per trade
        - You can adjust it based on your risk appetite, current portfolio exposure, market volatility...
        """)

    with col2:
        st.markdown("""
        ### 🤝 Step 4: Client Decision
        
        The client will respond with one of three actions:
        - **✅ BUY** (hits your ask) → You SELL the option
        - **✅ SELL** (hits your bid) → You BUY the option
        - **❌ PASS** → No trade executed
        
        If a trade is executed:
        - The position is added to your **book**
        - Your **P&L** updates based on the spread captured
        - Your **Greeks** (Delta, Gamma, Vega, Theta) update
        - Your **cash** and **portfolio value** adjust
        """)

    st.markdown("---")

    # Steps 5 & 6
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🛡️ Step 5: Manage Your Risks

        Monitor your exposure in the **"Risk Dashboard"**:
        """)

        greeks_df = pd.DataFrame({
            "Greek": ["**Delta**", "**Gamma**", "**Vega**", "**Theta**"],
            "What It Measures": [
                "Directional risk (price sensitivity)",
                "Delta change rate",
                "Volatility risk",
                "Time decay"
            ],
            "How to Hedge": [
                "Trade stocks or opposite options",
                "Trade options to offset",
                "Trade options with opposite Vega",
                "Manage expiration dates"
            ]
        })

        st.table(greeks_df)

        st.markdown("""
        **🎯 Delta Hedging Tool** (Located in **"Trading Shares"** panel):
        - Shows **recommended hedge** in shares to neutralize Delta
        - Stocks are Delta-1 instruments (perfect for hedging directional risk)
        - Execute stock trades to rebalance your Delta to ~0
        """)

    with col2:
        st.markdown("""
        ### 📈 Step 6: Option trading
        
        Access the **"Trading Options"** tab to:
        - Execute trade vanilla options (Calls/Puts) or option strategies (Straddles, Strangles, ...)
        - Rebalance your Greeks proactively
        - Take directional or volatility views
        
        **Use cases:**
        - Your Gamma is too high → sell some options
        - Your Vega is too negative → buy some options
        - You want to flatten your book before game end
        
        Note that all your trades must respect your **cash position** constraints.
        """)

    st.markdown('<div class="info-box"><b>💡 Pro Tip:</b> Keep your Delta near zero to avoid directional risk. Use the recommended hedge feature!</div>', unsafe_allow_html=True)
   
    st.markdown("---")

    # Game Interface Guide
    st.markdown('<p class="section-header">🖥️ Understanding Your Dashboard</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Top Metrics (Always Visible)
        
        **Key Performance Indicators:**
        - **Stock Price**: Current underlying price
        - **P&L**: Your total profit/loss
        - **Portfolio Value**: Cash + positions value
        - **Cash**: Available buying power
        
        **Live Charts:**
        - **📈 Price Chart**: Real-time stock movement
        - **💰 P&L Evolution**: Your profit over time
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Trading Tools
        
        **Options Pricer:**
        - Price any option or strategy
        - View Greeks before quoting
        
        **Trading Shares:**
        - Delta hedge calculator
        - Recommended position size
        
        **Current Positions:**
        - Live book display
        """)
    
    st.markdown("---")

    # Strategy Tips
    st.markdown('<p class="section-header">💡 Tips for the first games\'s strategies</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Start Conservative:**
        1. Quote close to fair value (pricer price)
        2. Use moderate spreads (10-15% of option value)
        3. Delta hedge after every trade
        4. Monitor risk Greeks
        """)

    with col2:
        st.markdown("""
        **Basic Workflow:**
        1. ✅ Client request arrives
        2. ✅ Price in Pricer and quote the bid/ask 
        3. ✅ If trade executes → Delta hedge 
        4. ✅ Monitor Greeks dashboard
        """)

    with col3:
        st.markdown("""
        **Golden Rules:**
        - 🛡️ Keep Delta near zero
        - 📊 Don't let Gamma explode
        """)
    
    st.markdown('<div class="warning-box"><b>⚠️ Common Mistakes to Avoid:</b><br>• Ignoring Delta → huge directional losses<br>• Wrong adjustment of volatility → arbitraged by clients<br></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    # Key Concepts
    st.markdown('<p class="section-header">📚 Key Concepts Explained</p>', unsafe_allow_html=True)
    
    with st.expander("💵 Bid-Ask Spread & Market Making", expanded=False):
        st.markdown("""
        **How you make money as a market maker:**
        
        You buy low (bid) and sell high (ask), capturing the spread:
        
        **Example:**
        - Client wants to buy a Call option
        - Fair value (from pricer): $5.00
        - You quote: Bid = $4.80, Ask = $5.20 (spread = $0.40)
        - Client buys at your ask ($5.20)
        - You capture $0.20 premium over fair value
        - Later, you hedge or offset the position
        
        **💰 Profit = Spread captured + Hedging P&L**
        
        ⚠️ **Trade-offs:**
        - Wide spread → More profit per trade but fewer trades (clients pass)
        - Tight spread → More trades but lower profit margins
        """)
    
    with st.expander("📊 The Greeks: Your Risk Metrics", expanded=False):
        st.markdown("""
        **Delta (Δ):** Directional risk
        - Measures option price change per $1 stock move
        - Call Delta: 0 to 1 | Put Delta: -1 to 0
        - **Portfolio Delta**: Sum of all positions' Deltas
        - **Hedge with**: Stocks (Delta = 1) or opposite options
        
        **Gamma (Γ):** Delta sensitivity
        - Measures how fast Delta changes
        - High Gamma → Delta changes rapidly → harder to hedge
        - Long options → Positive Gamma
        - Short options → Negative Gamma
        
        **Vega (ν):** Volatility risk
        - Measures P&L change per 1% volatility move
        - Long options → Positive Vega (profit if vol rises)
        - Short options → Negative Vega (profit if vol falls)
        - **Critical**: Mispricing vol causes biggest losses!
        
        **Theta (Θ):** Time decay
        - Daily P&L from time passing
        - Long options → Negative Theta (lose value daily)
        - Short options → Positive Theta (gain value daily)
        - Accelerates near expiration
        """)
    
    with st.expander("🎯 Delta Hedging Strategy", expanded=False):
        st.markdown("""
        **Why hedge Delta?**
        - Delta measures directional exposure
        - Unhedged Delta = betting on stock direction
        - Market makers aim to be **Delta neutral** (no directional bet)
        
        **How to hedge:**
        
        1. **Check your Portfolio Delta** (in Risk Dashboard)
        2. **Use the recommended hedge** (in Trading Shares panel)
        3. **Execute the stock trade**:
           - Portfolio Delta +100 → Sell 100 shares
           - Portfolio Delta -50 → Buy 50 shares
           - Portfolio Delta ~0 → No hedge needed
        
        **Example:**
        - You sold 1 Call (Delta = 0.60 per contract)
        - 100 contracts sold → Portfolio Delta = -60
        - Recommended hedge: **Buy 60 shares**
        - After hedge: Portfolio Delta ≈ 0 ✅
        
        **⚠️ Note:** Delta changes (Gamma), so rehedge regularly!
        """)
    
    with st.expander("🔮 Volatility: Your Secret Weapon", expanded=False):
        st.markdown("""
        **Why volatility matters:**
        - Options are primarily **volatility instruments**
        - Higher vol → Higher option prices
        - Lower vol → Lower option prices
        
        **Your edge as a market maker:**
        - Clients give you Strike + Maturity
        - **YOU decide if you want to adjust the volatility** to price with
        - If you misestimate → losses
        
        **Volatility strategies:**
        
        **Market is calm:**
        - Quote with lower vol
        - Sell options (collect premium)
        - Positive Theta (time decay profits)
        
        **Market is volatile:**
        - Quote with higher vol
        - Widen spreads (more risk = more compensation)
        - Watch for vol spikes
        
        **⚠️ Danger:**
        - Quote vol too low → clients arbitrage you
        - Quote vol too high → no trades (clients pass)
        - **Balance is key!**
        """)
    
    with st.expander("📦 Position Management", expanded=False):
        st.markdown("""
        **Your book tracks:**
        - All open positions (long/short)
        - Net Greeks exposure
        - Realized P&L (closed trades)
        
        **Position limits:**
        - Cash constraint (cannot trade beyond buying power)
        
        **Closing positions:**
        - Trade opposite direction (buy to close shorts, sell to close longs)
        - Use Trading Options tab
        - Or wait for client requests in opposite direction
        
        **End-of-game considerations:**
        - Flatten positions before time runs out
        - Large open positions = directional bet on final price
        """)
    st.markdown("---")

    # Game Controls
    st.markdown('<p class="section-header">🎮 Game Controls & Features</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **⏸️ Pause Button**
        - Freeze the game temporarily
        - You can take a moment review your positions and plan your next moves
        """)
    
    with col2:
        st.markdown("""
        **🔄 Reset Button**
        - Start a new game and get a new underlying stock
        """)
    
    with col3:
        st.markdown("""
        **🔃 Refresh Button**
        - Located near progress bar
        - Use if trades don't appear
        - Syncs book and Greeks
        """)

    st.markdown("---")
   

    # Footer with start button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎮 START TRADING", type="primary", use_container_width=True, key="start_game_btn"):
            st.session_state.show_rules = False
            st.rerun()

    st.markdown("<p style='text-align: center; color: #666; margin-top: 20px;'>Good luck, and may the Greeks be in your favor! 🎯</p>", unsafe_allow_html=True)