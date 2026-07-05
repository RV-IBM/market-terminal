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
                    # 1. Handle Window Selection
                    if window_selection == "90 Days": 
                        filtered_hist = full_hist.last("90D")
                    elif window_selection == "180 Days": 
                        filtered_hist = full_hist.last("180D")
                    elif window_selection == "Year-To-Date (YTD)":
                        from datetime import datetime
                        filtered_hist = full_hist[full_hist.index.year == datetime.now().year]
                    else: 
                        filtered_hist = full_hist.copy()
    
                    # 2. Calculate Technicals
                    full_hist['SMA_50'] = full_hist['Close'].rolling(window=50).mean()
                    filtered_hist['SMA_50'] = full_hist['SMA_50'].loc[filtered_hist.index]
    
                    # 3. Render Chart
                    st.subheader(f"📊 {pro_ticker.upper()} DETAILED ALGORITHMIC PROFILE ({window_selection})")
                    st.line_chart(filtered_hist[['Close', 'SMA_50']])
    
                    # 4. Render Microstructure Metrics
                    st.subheader("📄 DETAILED LIVE MICROSTRUCTURE DATA")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Day High", f"${info.get('dayHigh', 0):,.2f}")
                    m2.metric("Day Low", f"${info.get('dayLow', 0):,.2f}")
                    m3.metric("Avg Volume (10d)", f"{info.get('averageDailyVolume10Day', 0):,}")
                    m4.metric("Beta Coefficient", f"{info.get('beta', 'N/A')}")
    
                    st.divider()
                    
                    # 5. Risk & Breakout Layout
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
            
                    with col_break:
                        st.subheader("TECHNICAL BREAKOUT THRESHOLDS")
                        with st.container(border=True):
                            current_price = filtered_hist['Close'].iloc[-1]
                            resistance = info.get('fiftyTwoWeekHigh', current_price * 1.05)
                            support = filtered_hist['Close'].min()
                            st.write(f"**Macro Resistance Ceiling:** `${resistance:,.2f}`")
                            st.write(f"**Dynamic Baseline Support:** `${support:,.2f}`")
                            st.write(f"**Velocity Continuation Trigger:** `${(resistance * 1.01):,.2f}`")
            
                else:
                    st.warning(f"⚠️ SYSTEM NOTIFICATION: Live telemetry for {pro_ticker} is temporarily unavailable. Please try another ticker or wait a moment.")
            
            except Exception as e:
                st.error(f"⚠️ INTERFACE ERROR: {e}")
            
            
            # ====================================================================
            # NEURAL VERDICT SECTION (Sits safely outside the upper telemetry block)
            # ====================================================================
            st.divider()
            
            if st.button("RUN DEEP-DIVE NEURAL VERDICT"):
                info, hist = get_stock_data_func(pro_ticker, range_type="pro")
                
                with st.spinner("Decoding Advanced Quant Telemetry..."):
                    url = st.secrets["PIPEDREAM_URL"]
                    
                    try:
                        res = requests.post(url, json={"ticker": pro_ticker, "tier": "pro"}, timeout=45)
                        
                        if res.status_code == 200:
                            st.success("⚡ PRO LEVEL NEURAL LINK ESTABLISHED")
                            with st.container(border=True):
                                raw_prediction = res.json().get("prediction", "No telemetry data.")
                                # Initialize our final display string
                                clean_output = ""
                                
                                try:
                                    # If Pipedream sent back a double-serialized string, parse it into a dict
                                    if isinstance(raw_prediction, str):
                                        import ast
                                        parsed_dict = ast.literal_eval(raw_prediction)
                                    else:
                                        parsed_dict = raw_prediction
                                    
                                    # robust extraction targeting your specific JSON payload structure
                                    if isinstance(parsed_dict, dict):
                                        if "candidates" in parsed_dict and len(parsed_dict["candidates"]) > 0:
                                            candidate = parsed_dict["candidates"][0]
                                            
                                            # Check standard nested structure
                                            if "content" in candidate and "parts" in candidate["content"]:
                                                clean_output = candidate["content"]["parts"][0]["text"]
                                            # Check if it's flat inside the candidate (e.g., candidate['text'])
                                            elif "text" in candidate:
                                                clean_output = candidate["text"]
                                            # Check if parts is flat inside the candidate
                                            elif "parts" in candidate:
                                                clean_output = candidate["parts"][0].get("text", str(candidate))
                                            else:
                                                # Fallback: Look for any key named 'text' or 'prediction' inside the dict
                                                clean_output = parsed_dict.get("text", parsed_dict.get("output", str(raw_prediction)))
                                        else:
                                            clean_output = parsed_dict.get("text", str(parsed_dict))
                                    else:
                                        clean_output = str(raw_prediction)
                                        
                                except Exception as parse_err:
            # Fallback if ast parsing completely chokes
            clean_output = str(raw_prediction)

        # ---------------------------------------------------------
        # NEW PRO CYBER DASHBOARD RENDERING ENGINE
        # ---------------------------------------------------------
        if isinstance(clean_output, str):
            clean_output = clean_output.replace("\\n", "\n").replace("\\\"", "\"")
            
            import re
            # Scrub reasoning models <think> tags if they exist
            clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
            
            # TEXT COLORIZATION ENGINE
            def cyber_highlight(text):
                if not isinstance(text, str):
                    return str(text)
                # Neon Green for positive market sentiment
                text = re.sub(r'(?i)(bullish|support|rebound|growth|outperform|buy|upside|momentum)', r'<span style="color: #00ff88; text-shadow: 0 0 5px #00ff88;">\1</span>', text)
                # Neon Red for negative market sentiment
                text = re.sub(r'(?i)(bearish|resistance|contraction|downgrade|sell|downside|risk|breakdown)', r'<span style="color: #ff3333; text-shadow: 0 0 5px #ff3333;">\1</span>', text)
                return text

            # SMART JSON DETECTOR (Failsafe for cut-off AI responses)
            import json
            json_obj = None
            
            if "{" in clean_output:
                try:
                    start_idx = clean_output.find("{")
                    end_idx = clean_output.rfind("}") + 1
                    possible_json = clean_output[start_idx:end_idx]
                    json_obj = json.loads(possible_json)
                except:
                    # If JSON is cut off mid-sentence, this catches the crash
                    json_obj = None

            # RENDER THE PREMIUM BLACK/BLUE UI
            if json_obj:
                dashboard_html = """
                <style>
                    .cyber-card { background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Courier New', Courier, monospace;}
                    .cyber-title { color: #00e5ff; font-size: 1.1em; font-weight: bold; border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 10px; text-transform: uppercase;}
                    .cyber-key { color: #8892b0; font-weight: bold; font-size: 0.9em;}
                    .cyber-value { color: #e2e8f0; font-size: 0.95em; margin-bottom: 10px; display: block;}
                </style>
                <div style="padding: 10px 0;">
                """
                
                # Recursively build cards for nested data
                def build_html(obj):
                    html = ""
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, (dict, list)):
                                html += f"<div class='cyber-card'><div class='cyber-title'>{k}</div>{build_html(v)}</div>"
                            else:
                                html += f"<div><span class='cyber-key'>{k}: </span><span class='cyber-value'>{cyber_highlight(str(v))}</span></div>"
                    elif isinstance(obj, list):
                        for item in obj:
                            html += f"<div style='margin-left: 15px; border-left: 1px solid #1e293b; padding-left: 10px;'>{build_html(item)}</div>"
                    else:
                        html += f"<span class='cyber-value'>{cyber_highlight(str(obj))}</span>"
                    return html
                
                dashboard_html += build_html(json_obj) + "</div>"
                st.markdown(dashboard_html, unsafe_allow_html=True)
            else:
                # If the AI response was pure text or cut off severely, render it safely with highlights
                fallback_html = f"<div style='background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 15px; font-family: \"Courier New\", Courier, monospace; color: #e2e8f0;'>{cyber_highlight(clean_output)}</div>"
                st.markdown(fallback_html, unsafe_allow_html=True)
        else:
            st.write(clean_output)
    else:
        st.error("NEURAL LINK FAILURE")
                            
                    except requests.exceptions.Timeout:
                        st.warning("🦤 TELEMETRY DELAY: Complex matrix generation took longer than 45 seconds. Please click again to retry.")
                    except requests.exceptions.RequestException:
                        st.error("⚠️ PIPELINE ERROR: Interface gateway disconnected. Please check your network connection.")
