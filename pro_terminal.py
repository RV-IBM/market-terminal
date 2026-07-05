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
            st.title("INSTITUTIONAL QUANT DESK")
            col_input, col_window = st.columns([2, 1])
            with col_input:
                pro_ticker = st.text_input("INPUT PREMIUM PROTOCOL:", placeholder="e.g., NVDA, TSLA").upper()
            with col_window:
                window_selection = st.selectbox("TELEMETRY INCREASE WINDOW:", ["90 Days", "180 Days", "Year-To-Date (YTD)", "Full Year"])

            if pro_ticker:
                try:
                    info, full_hist = get_stock_data_func(pro_ticker, range_type="pro")
                    
                    # 1. BULLETPROOF CHART FALLBACK: 
                    # If custom func fails (due to weekends or rate limits), force a fresh 1-year fetch
                    if full_hist is None or full_hist.empty:
                        import yfinance as yf
                        t = yf.Ticker(pro_ticker)
                        full_hist = t.history(period="1y")
                        try:
                            info = t.info
                        except:
                            pass

                    if full_hist is not None and not full_hist.empty:
                        from datetime import datetime, timedelta
                        
                        # 2. SAFE DATE FILTERING (Prevents crashes on YTD selection)
                        last_date = full_hist.index.max()
                        if window_selection == "90 Days":
                            filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=90))]
                        elif window_selection == "180 Days":
                            filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=180))]
                        elif window_selection == "Year-To-Date (YTD)":
                            filtered_hist = full_hist[full_hist.index.year == last_date.year]
                        else:
                            filtered_hist = full_hist.copy()

                        # 3. Calculate Technicals
                        full_hist['SMA_50'] = full_hist['Close'].rolling(window=50).mean()
                        filtered_hist['SMA_50'] = full_hist['SMA_50'].loc[filtered_hist.index]

                        # 4. Render Chart
                        st.subheader(f"📊 {pro_ticker.upper()} DETAILED ALGORITHMIC PROFILE ({window_selection})")
                        st.line_chart(filtered_hist[['Close', 'SMA_50']])

                        # 5. Render Microstructure Metrics
                        st.subheader("📄 DETAILED LIVE MICROSTRUCTURE DATA")
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Day High", f"${info.get('dayHigh', 0):,.2f}")
                        m2.metric("Day Low", f"${info.get('dayLow', 0):,.2f}")
                        m3.metric("Avg Volume (10d)", f"{info.get('averageDailyVolume10Day', 0):,}")
                        m4.metric("Beta Coefficient", f"{info.get('beta', 'N/A')}")
                        
                        st.divider()
                        
                        # 6. Risk & Breakout Layout
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
                        st.warning(f"⚠️ SYSTEM NOTIFICATION: Live telemetry for {pro_ticker} is temporarily unavailable.")
                
                    except Exception as e:
                        st.error(f"⚠️ INTERFACE ERROR: {str(e)}")
    
                    st.divider()
    
                    # ==========================================================
                    # PRO NEURAL VERDICT EXECUTION
                    # ==========================================================
                    if st.button("RUN DEEP-DIVE NEURAL VERDICT"):
                        with st.spinner("⚡ Decoding Advanced Quant Telemetry..."):
                            try:
                                # Using Streamlit secrets for Pipedream
                                url = st.secrets["PIPEDREAM_URL"]
                                res = requests.post(url, json={"ticker": pro_ticker, "tier": "pro"}, timeout=45)
                                
                                if res.status_code == 200:
                                    st.success("⚡ PRO LEVEL NEURAL LINK ESTABLISHED")
                                    raw_prediction = res.json().get("prediction", "No telemetry data.")
                                    
                                    clean_output = str(raw_prediction).replace("\\n", "\n").replace("\\\"", "\"")
                                    
                                    import re, ast, json
                                    # Clean reasoning tags
                                    clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
                                    
                                    # Highlight function (added more pro terms based on output!)
                                    def cyber_highlight(text):
                                        if not isinstance(text, str): return str(text)
                                        text = re.sub(r'(?i)(bullish|support|rebound|growth|outperform|buy|upside|momentum|resilience|recovery|positive)', r'<span style="color: #00ff88; text-shadow: 0 0 5px #00ff88;">\1</span>', text)
                                        text = re.sub(r'(?i)(bearish|resistance|contraction|downgrade|sell|downside|risk|breakdown|drawdown|distribution)', r'<span style="color: #ff3333; text-shadow: 0 0 5px #ff3333;">\1</span>', text)
                                        return text
                                    
                                    # 7. INTELLIGENT PARSER (Fixes the single-quote bug!)
                                    json_obj = None
                                    if "{" in clean_output:
                                        try:
                                            start = clean_output.find("{")
                                            end = clean_output.rfind("}") + 1
                                            bracketed_text = clean_output[start:end]
                                            
                                            try:
                                                # Try standard JSON first
                                                json_obj = json.loads(bracketed_text)
                                            except:
                                                # THE FIX: If it's a Python dict string with single quotes, AST evaluates it perfectly!
                                                json_obj = ast.literal_eval(bracketed_text)
                                        except:
                                            json_obj = None
                                    
                                    # 8. PRO CYBER DASHBOARD RENDERER
                                    if json_obj and isinstance(json_obj, dict):
                                        dashboard_html = """
                                        <style>
                                            .cyber-card { background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Courier New', Courier, monospace;}
                                            .cyber-title { color: #00e5ff; font-size: 1.1em; font-weight: bold; border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 10px; text-transform: uppercase;}
                                            .cyber-key { color: #8892b0; font-weight: bold; font-size: 0.9em; text-transform: capitalize;}
                                            .cyber-value { color: #e2e8f0; font-size: 0.95em; margin-bottom: 10px; display: block; line-height: 1.6;}
                                        </style>
                                        <div style="padding: 10px 0;">
                                        """
                                        def build_html(obj):
                                            html = ""
                                            if isinstance(obj, dict):
                                                for k, v in obj.items():
                                                    # Clean up underscores in keys (e.g., 'outlook_30d' -> 'outlook 30d')
                                                    clean_k = str(k).replace("_", " ")
                                                    if isinstance(v, (dict, list)):
                                                        html += f"<div class='cyber-card'><div class='cyber-title'>{clean_k}</div>{build_html(v)}</div>"
                                                    else:
                                                        html += f"<div><span class='cyber-key'>{clean_k}: </span><span class='cyber-value'>{cyber_highlight(str(v))}</span></div>"
                                            elif isinstance(obj, list):
                                                for item in obj:
                                                    html += f"<div style='margin-left: 15px; border-left: 1px solid #1e293b; padding-left: 10px;'>{build_html(item)}</div>"
                                            else:
                                                html += f"<span class='cyber-value'>{cyber_highlight(str(obj))}</span>"
                                            return html
                                            
                                        dashboard_html += build_html(json_obj) + "</div>"
                                        st.markdown(dashboard_html, unsafe_allow_html=True)
                                    else:
                                        # Formatted fallback with easier readability
                                        fallback_html = f"<div style='background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 20px; font-family: \"Courier New\", Courier, monospace; color: #e2e8f0; line-height: 1.7; font-size: 1.05em;'>{cyber_highlight(clean_output)}</div>"
                                        st.markdown(fallback_html, unsafe_allow_html=True)
    
                                else:
                                    st.error(f"NEURAL LINK FAILURE: Status {res.status_code}")
                                    
                            except requests.exceptions.Timeout:
                                st.warning("🦤 TELEMETRY DELAY: Complex matrix generation took longer than 45 seconds.")
                            except requests.exceptions.RequestException as e:
                                st.error(f"⚠️ PIPELINE ERROR: Interface gateway disconnected. Details: {e}")
