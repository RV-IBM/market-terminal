import streamlit as st
import requests
import pandas as pd
import yfinance as yf
import re
import json
import ast
from datetime import datetime, timedelta

def get_final_verdict(data_obj, raw_text):
    """Analyzes AI output to determine a strict BUY, HOLD, or SELL conclusion."""
    search_text = (str(data_obj) + " " + str(raw_text)).upper()
    
    # Explicit conclusion checks
    if "CONCLUSION: BUY" in search_text or "'BUY'" in search_text or '"BUY"' in search_text or "RATING: BUY" in search_text:
        return "BUY", "#00ff88"
    if "CONCLUSION: SELL" in search_text or "'SELL'" in search_text or '"SELL"' in search_text or "RATING: SELL" in search_text:
        return "SELL", "#ff3333"
    if "CONCLUSION: HOLD" in search_text or "'HOLD'" in search_text or '"HOLD"' in search_text or "RATING: HOLD" in search_text:
        return "HOLD", "#ffaa00"
        
    # Sentiment Fallback
    bullish = sum(search_text.count(w) for w in ["BULL", "BUY", "ACCUMULATE", "OUTPERFORM", "UPWARD"])
    bearish = sum(search_text.count(w) for w in ["BEAR", "SELL", "REDUCE", "UNDERPERFORM", "DOWNWARD"])
    
    if bullish > bearish * 1.5: return "BUY", "#00ff88"
    elif bearish > bullish * 1.5: return "SELL", "#ff3333"
    return "HOLD", "#ffaa00"

def render_pro_terminal(is_premium, get_stock_data_func):
    stripe_link = st.secrets.get("STRIPE_CHECKOUT_URL", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00")
    
    # ==========================================
    # ACCESS CONTROL (UI CONSISTENCY)
    # ==========================================
    if not is_premium:
        # Reverting to the clean layout structure observed in image_6e35eb.png
        st.markdown("""
        <div style="border: 2px dashed #ff3333; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <h1 style='color: #00e5ff; font-family: monospace;'>🔒 ACCESS DENIED: LEVEL 2 CLEARANCE REQUIRED</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Make sure Stripe URL actually exists
        if not stripe_link:
            st.error("Stripe checkout link is not configured.")
            return

        # Display working Stripe button
        st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00", use_container_width=True)
        return

    # ==========================================
    # INSTITUTIONAL QUANT DESK UI
    # ==========================================
    st.title("INSTITUTIONAL QUANT DESK")
    col_input, col_window = st.columns([2, 1])
    with col_input:
        pro_ticker = st.text_input("INPUT PREMIUM PROTOCOL:", placeholder="e.g., NVDA, TSLA").upper()
    with col_window:
        window_selection = st.selectbox("TELEMETRY INCREASE WINDOW:", ["90 Days", "180 Days", "Year-To-Date (YTD)", "Full Year"])

    if pro_ticker:
        try:
            # 1. FORCE 1-YEAR HISTORY FETCH DIRECTLY FIRST
            import yfinance as yf
            t = yf.Ticker(pro_ticker)
            full_hist = t.history(period="1y")
            
            # 2. GRAB METADATA FROM HELPER
            try:
                info, fallback_hist = get_stock_data_func(pro_ticker, range_type="pro")
            except Exception:
                info = t.info if hasattr(t, 'info') else {}
                fallback_hist = None
            
            # 3. ONLY USE HELPER HISTORY IF YFINANCE FAILS
            if full_hist is None or full_hist.empty:
                full_hist = fallback_hist

            if full_hist is not None and not full_hist.empty:
                from datetime import datetime, timedelta
                last_date = full_hist.index.max()
                if window_selection == "90 Days":
                    filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=90))]
                elif window_selection == "180 Days":
                    filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=180))]
                elif window_selection == "Year-To-Date (YTD)":
                    filtered_hist = full_hist[full_hist.index.year == last_date.year]
                else:
                    filtered_hist = full_hist.copy()

                # Render Charts
                st.subheader(f"{pro_ticker.upper()} DETAILED ALGORITHMIC PROFILE")
                st.line_chart(filtered_hist['Close'])

                st.subheader("DETAILED LIVE MICROSTRUCTURE DATA")
                m1, m2, m3, m4 = st.columns(4)
                
                curr_price = filtered_hist['Close'].iloc[-1]
                m1.metric("Day High", f"${info.get('dayHigh', curr_price):,.2f}")
                m2.metric("Day Low", f"${info.get('dayLow', curr_price):,.2f}")
                m3.metric("Avg Volume (10d)", f"{info.get('averageDailyVolume10Day', 0):,}")
                m4.metric("Beta", f"{info.get('beta', 1.0):.2f}")
                
                st.divider()
                
                col_risk, col_break = st.columns(2)
                with col_risk:
                    st.subheader("ASYMMETRIC RISK MATRIX")
                    
                    target_price = info.get('targetMeanPrice') or (curr_price * 1.15)
                    upside = ((target_price - curr_price) / curr_price) * 100
                    fifty_two_low = info.get('fiftyTwoWeekLow') or (curr_price * 0.8)
                    risk = ((curr_price - fifty_two_low) / curr_price) * 100
                    ratio = abs(upside / risk) if risk != 0 else 0

                    st.markdown(f"""
                    | Metric | Value |
                    | :--- | :--- |
                    | **Upside Potential** | {upside:.2f}% |
                    | **Tail Risk Exposure** | {risk:.2f}% |
                    | **Risk/Reward Ratio** | **{ratio:.2f}x** |
                    """)

                with col_break:
                    st.subheader("TECHNICAL THRESHOLDS")
                    resistance = info.get('fiftyTwoWeekHigh', curr_price * 1.05)
                    support = info.get('fiftyTwoWeekLow', curr_price * 0.95)
                    st.write(f"**Resistance Ceiling:** `${resistance:,.2f}`")
                    st.write(f"**Baseline Support:** `${support:,.2f}`")
                    st.write(f"**Continuation Trigger:** `${(resistance * 1.01):,.2f}`")

            else:
                st.warning(f"⚠️ Live telemetry for {pro_ticker} unavailable.")
        
        except Exception as e:
            st.error(f"⚠️ INTERFACE ERROR: {str(e)}")

        st.divider()

        if st.button("RUN DEEP-DIVE NEURAL VERDICT"):
            with st.spinner("⚡ Decoding Advanced Quant Telemetry..."):
                try:
                    url = st.secrets.get("PIPEDREAM_URL", "")
                    if url:
                        res = requests.post(url, json={"ticker": pro_ticker, "tier": "pro"}, timeout=45)
                        raw_prediction = res.json().get("prediction", "No data.") if res.status_code == 200 else "Link Failure"
                    else:
                        raw_prediction = "{'error': 'Missing API Key'}"
                    
                    clean_output = str(raw_prediction).replace("\\n", "\n").replace("\\\"", "\"")
                    clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
                    
                    if "```json" in clean_output.lower():
                        try:
                            clean_output = clean_output.split("```json")[1].split("```")[0].strip()
                        except Exception:
                            pass
                    elif "```" in clean_output:
                        try:
                            clean_output = clean_output.split("```")[1].split("```")[0].strip()
                        except Exception:
                            pass
                    
                    def cyber_highlight(text):
                        if not isinstance(text, str): return str(text)
                        text = re.sub(r'(?i)(bullish|support|rebound|growth|outperform|buy|upside|momentum)', r'<span style="color: #00ff88; text-shadow: 0 0 5px #00ff88;">\1</span>', text)
                        text = re.sub(r'(?i)(bearish|resistance|contraction|downgrade|sell|downside|risk|breakdown)', r'<span style="color: #ff3333; text-shadow: 0 0 5px #ff3333;">\1</span>', text)
                        return text

                    json_obj = None
                    if "{" in clean_output:
                        try:
                            start, end = clean_output.find("{"), clean_output.rfind("}") + 1
                            bracketed_text = clean_output[start:end]
                            try:
                                json_obj = json.loads(bracketed_text)
                            except Exception:
                                json_obj = ast.literal_eval(bracketed_text)
                        except Exception:
                            json_obj = None
                    
                    if isinstance(json_obj, dict):
                        if "alpha_gen_intelligence" in json_obj:
                            data = json_obj["alpha_gen_intelligence"]
                            
                            verdict, v_color = get_final_verdict(json_obj, clean_output)
                            
                            st.markdown(f"""
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                                <h3 style="margin: 0;">🧠 Neural Analysis: {pro_ticker.upper()}</h3>
                                <div style="border: 2px solid {v_color}; background: rgba(0,0,0,0.3); padding: 6px 16px; border-radius: 6px; font-weight: bold; color: {v_color}; font-size: 1.2rem; letter-spacing: 0.1em; box-shadow: 0 0 12px {v_color}40;">
                                    {verdict}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            outlook = data.get('outlook_30d', 'Neutral')
                            if "bull" in outlook.lower() or "up" in outlook.lower():
                                st.success(f"**30-Day Trajectory:** {outlook} 🚀")
                            elif "bear" in outlook.lower() or "down" in outlook.lower():
                                st.error(f"**30-Day Trajectory:** {outlook} 🔻")
                            else:
                                st.warning(f"**30-Day Trajectory:** {outlook} ⚖️")
                                
                            quant = data.get("quantitative_trend_telemetry", {})
                            sr = quant.get("support_resistance", {})
                            exec_data = data.get("strategic_execution", {})
                            
                            c1, c2, c3 = st.columns(3)
                            c1.metric("🛡️ Primary Support", f"${sr.get('primary_support', 'N/A')}")
                            c2.metric("🎯 Primary Resistance", f"${sr.get('primary_resistance', 'N/A')}")
                            c3.metric("🤖 AI Confidence", f"{exec_data.get('confidence_score', 'N/A')}%")
                            
                            with st.expander("📊 Quantitative Trend Telemetry", expanded=True):
                                st.markdown("**Delta Summary**")
                                st.info(quant.get("delta_summary", "N/A"))
                                st.markdown("**Volatility Profile**")
                                st.warning(quant.get("volatility_profile", "N/A"))
                                
                            with st.expander("🌐 Contextual Intelligence", expanded=True):
                                st.write(cyber_highlight(data.get("contextual_intelligence", "N/A")), unsafe_allow_html=True)
                                
                            if "neural_signature" in exec_data:
                                st.caption(f"Neural Signature: `{exec_data.get('neural_signature')}`")
                        else:
                            verdict, v_color = get_final_verdict(json_obj, clean_output)
                            
                            st.markdown(f"""
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                                <h3 style="margin: 0;">🧠 Neural Analysis: {pro_ticker.upper()}</h3>
                                <div style="border: 2px solid {v_color}; background: rgba(0,0,0,0.3); padding: 6px 16px; border-radius: 6px; font-weight: bold; color: {v_color}; font-size: 1.2rem; letter-spacing: 0.1em; box-shadow: 0 0 12px {v_color}40;">
                                    {verdict}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            dashboard_html = "<style>.cyber-card { background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Courier New', monospace; line-height: 1.6;}</style><div style='padding: 10px 0;'>"
                            def build_html(obj):
                                html = ""
                                if isinstance(obj, dict):
                                    for k, v in obj.items():
                                        clean_k = str(k).replace("_", " ").title()
                                        if isinstance(v, (dict, list)):
                                            html += f"<div class='cyber-card'><div style='color: #00e5ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-bottom: 10px;'>{clean_k}</div>{build_html(v)}</div>"
                                        else:
                                            html += f"<div><span style='color: #8892b0; font-weight: bold;'>{clean_k}: </span><span style='color: #e2e8f0;'>{cyber_highlight(str(v))}</span></div>"
                                elif isinstance(obj, list):
                                    for item in obj: html += f"<div style='margin-left: 15px; border-left: 1px solid #1e293b; padding-left: 10px;'>{build_html(item)}</div>"
                                else:
                                    html += f"<span style='color: #e2e8f0;'>{cyber_highlight(str(obj))}</span>"
                                return html
                            st.markdown(dashboard_html + build_html(json_obj) + "</div>", unsafe_allow_html=True)
                    else:
                        verdict, v_color = get_final_verdict(None, clean_output)
                        st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                            <h3 style="margin: 0;">🧠 Neural Analysis: {pro_ticker.upper()}</h3>
                            <div style="border: 2px solid {v_color}; background: rgba(0,0,0,0.3); padding: 6px 16px; border-radius: 6px; font-weight: bold; color: {v_color}; font-size: 1.2rem; letter-spacing: 0.1em; box-shadow: 0 0 12px {v_color}40;">
                                {verdict}
                            </div>
                        </div>
                        <div style='background: #0a0e17; padding: 20px; color: #e2e8f0; font-family: monospace; white-space: pre-wrap; line-height: 1.6;'>{cyber_highlight(clean_output)}</div>
                        """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Pipeline error: {e}")
