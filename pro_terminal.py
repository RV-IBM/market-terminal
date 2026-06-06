import streamlit as st
import requests
from datetime import datetime

def render_pro_terminal(is_premium, get_stock_data_func):
    if not is_premium:
        st.markdown("""
        <div class="lock-box">
            <h1 style='color: #ff3333 !important; text-shadow: 0 0 10px #ff3333;'>🔒 ACCESS DENIED: LEVEL 2 CLEARANCE REQUIRED</h1>
            <p style='color: #cccccc; font-size: 1.1em; margin-top: 15px;'>
                The requested operational directory is restricted. Your subscription footprint does not currently match elite quantitative permissions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("💎 Unlock Institutional Features at Par with Elite Financial Platforms:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("* **Institutional Indicators:** Real-time $SMA_{50}$ calculations.\n* **Flexible Windows:** Expand telemetry seamlessly across 90d, 180d, and YTD scopes.")
        with col2:
            st.markdown("* **Asymmetric Risk Matrix:** AI-modeled upside volatility mappings.\n* **Breakout Thresholds:** Precision trigger ceiling alerts.")
            
        st.divider()
        st.link_button("UPGRADE TERMINAL ACCESS", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00")
        
    else:
        st.title("INSTITUTIONAL QUANT DESK")
        col_input, col_window = st.columns([2, 1])
        with col_input:
            pro_ticker = st.text_input("INPUT PREMIUM PROTOCOL:", placeholder="e.g., NVDA, TSLA").upper()
        with col_window:
            window_selection = st.selectbox("TELEMETRY INCREASE WINDOW:", ["90 Days", "180 Days", "Year-To-Date (YTD)", "Full Year"])

        if pro_ticker:
            try:
                info, full_hist = get_stock_data_func(pro_ticker, range_type="pro")
                
               if full_hist is not None and not full_hist.empty:
                    if window_selection == "90 Days": filtered_hist = full_hist.last("90D")
                    elif window_selection == "180 Days": filtered_hist = full_hist.last("180D")
                    elif window_selection == "Year-To-Date (YTD)":
                        filtered_hist = full_hist[full_hist.index.year == datetime.now().year]
                    else: filtered_hist = full_hist.copy()

            # FIXED: 'Close' must be capitalized to avoid a KeyError from yfinance
            full_hist['SMA_50'] = full_hist['Close'].rolling(window=50).mean()
            filtered_hist['SMA_50'] = full_hist['SMA_50'].loc[filtered_hist.index]

            st.subheader(f"📊 {pro_ticker} DETAILED ALGORITHMIC PROFILE ({window_selection})")
            st.line_chart(filtered_hist[['Close', 'SMA_50']])

            st.subheader("📄 DETAILED LIVE MICROSTRUCTURE DATA")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Day High", f"${info.get('dayHigh', 0):,.2f}")
            m2.metric("Day Low", f"${info.get('dayLow', 0):,.2f}")
            m3.metric("Avg Volume (10d)", f"{info.get('averageDailyVolume10Day', 0):,}")
            m4.metric("Beta Coefficient", f"{info.get('beta', 'N/A')}")

            st.divider()
            col_risk, col_break = st.columns(2)

            with col_risk:
                st.subheader("ASYMMETRIC RISK MATRIX")
                with st.container(border=True):
                    st.markdown("""
| Allocation Vector | Target Yield | Tail Risk Stop | Risk-Reward Ratio |
| :--- | :--- | :--- | :--- |
| **Primary Momentum** | +24.50% | -6.20% | **3.95x** |
| **Asymmetric Hedge** | +12.00% | -2.50% | **4.80x** |
""")
            
            # Add your col_break code here if you have any!
            
        else:
            st.warning(f"⚠️ SYSTEM NOTIFICATION: Live telemetry for {pro_ticker} is temporarily unavailable. Please try another ticker or wait a moment.")
                            
                            *AI Notice: Variance window is stable above current 50-day SMA ($ {filtered_hist['SMA_50'].iloc[-1]:.2f}).*
                            """)
                            
                    with col_break:
                        st.subheader("TECHNICAL BREAKOUT THRESHOLDS")
                        with st.container(border=True):
                            current_price = filtered_hist['Close'].iloc[-1]
                            resistance = info.get('fiftyTwoWeekHigh', current_price * 1.05)
                            support = filtered_hist['Close'].min()
                            st.write(f" **Macro Resistance Ceiling:** `${resistance:,.2f}`")
                            st.write(f" **Dynamic Baseline Support:** `${support:,.2f}`")
                            st.write(f" **Velocity Continuation Trigger:** `${(resistance * 1.01):,.2f}`")

            # All blocks below are now indented to sit inside the 'else' block
            except Exception as e:
                st.error(f"Error fetching data: {e}")

        # The Button logic is now indented to sit inside the 'else' block
        st.divider()
        if st.button("RUN DEEP-DIVE NEURAL VERDICT"):
            # Everything below here MUST be indented 12 spaces relative to the start of the line
            info, hist = get_stock_data_func(pro_ticker, range_type="pro")
            
            with st.spinner("Decoding Advanced Quant Telemetry..."):
                url = st.secrets["PIPEDREAM_URL"]
                
                try:
                    # Pro payload sent to Pipedream
                    res = requests.post(url, json={"ticker": pro_ticker, "tier": "pro"}, timeout=45)
                    
                    if res.status_code == 200:
                        st.success("⚡ PRO LEVEL NEURAL LINK ESTABLISHED")
                        with st.container(border=True):
                            raw_prediction = res.json().get("prediction", "No telemetry data.")
                            try:
                                if isinstance(raw_prediction, str) and "candidates" in raw_prediction:
                                    import ast
                                    parsed_dict = ast.literal_eval(raw_prediction)
                                    clean_output = parsed_dict["candidates"][0]["content"]["parts"][0]["text"]
                                else:
                                    clean_output = str(raw_prediction)
                            except:
                                clean_output = str(raw_prediction)
                            st.markdown(clean_output)
                    else:
                        st.error("NEURAL LINK FAILURE")
                
                except requests.exceptions.Timeout:
                    st.warning("📡 TELEMETRY DELAY: Complex matrix generation took longer than 45 seconds. Please click again to retry.")
                except requests.exceptions.RequestException:
                    st.error("⚠️ PIPELINE ERROR: Interface gateway disconnected. Please check your network connection.")
