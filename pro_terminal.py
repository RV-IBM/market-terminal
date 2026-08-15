import streamlit as st
import requests
import pandas as pd
import yfinance as yf
import re
import json
import ast
from datetime import datetime, timedelta

def sanitize_json_response(raw_text):
    """Strips reasoning/thinking tags and securely parses JSON from raw backend response."""
    clean_text = re.sub(r'<think>.*?</think>', '', str(raw_text), flags=re.DOTALL).strip()
    
    # Strip Markdown formatting blocks
    if "```json" in clean_text.lower():
        try:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        except Exception:
            pass
    elif "```" in clean_text:
        try:
            clean_text = clean_text.split("```")[1].split("```")[0].strip()
        except Exception:
            pass
            
    # Attempt to extract and load JSON
    if "{" in clean_text and "}" in clean_text:
        try:
            start = clean_text.find("{")
            end = clean_text.rfind("}") + 1
            json_substr = clean_text[start:end]
            try:
                return json.loads(json_substr), clean_text
            except Exception:
                # Fallback for single quotes or boolean mis-capitalization
                safe_str = json_substr.replace("'", '"').replace("True", "true").replace("False", "false")
                return json.loads(safe_str), clean_text
        except Exception:
            pass
            
    return None, clean_text

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

def safe_extract(data_obj, possible_keys, default="N/A"):
    """Recursively and aggressively searches a dictionary/list for fuzzy key matches."""
    if isinstance(data_obj, dict):
        for k in possible_keys:
            if k in data_obj and data_obj[k] not in [None, "", "N/A", "null", []]:
                val = data_obj[k]
                if isinstance(val, list) and len(val) > 0: return val[0]
                if not isinstance(val, (dict, list)): return val
        
        for k, v in data_obj.items():
            k_lower = str(k).lower()
            for pk in possible_keys:
                if pk.lower() in k_lower and v not in [None, "", "N/A", "null", []]:
                    if isinstance(v, list) and len(v) > 0:
                        if not isinstance(v[0], (dict, list)): return v[0]
                    elif not isinstance(v, (dict, list)): 
                        return v
                        
        for v in data_obj.values():
            res = safe_extract(v, possible_keys, None)
            if res is not None: return res
            
    elif isinstance(data_obj, list):
        for item in data_obj:
            res = safe_extract(item, possible_keys, None)
            if res is not None: return res
            
    return default

def cyber_highlight(text):
    """Highlights financial keywords in neon green or red."""
    if not isinstance(text, str): return str(text)
    text = re.sub(r'(?i)(bullish|support|rebound|growth|outperform|buy|upside|momentum|accumulate)', r'<span style="color: #00ff88; text-shadow: 0 0 5px rgba(0,255,136,0.3); font-weight:bold;">\1</span>', text)
    text = re.sub(r'(?i)(bearish|resistance|contraction|downgrade|sell|downside|risk|breakdown|reduce)', r'<span style="color: #ff3333; text-shadow: 0 0 5px rgba(255,51,51,0.3); font-weight:bold;">\1</span>', text)
    return text

def render_pro_terminal(is_premium, get_stock_data_func):
    stripe_link = st.secrets.get("STRIPE_CHECKOUT_URL", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00")
    
    # ==========================================
    # ACCESS CONTROL (UI CONSISTENCY)
    # ==========================================
    if not is_premium:
        st.markdown("""
        <div style="border: 2px dashed #ff3333; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <h1 style='color: #00e5ff; font-family: monospace;'>🔒 ACCESS DENIED: LEVEL 2 CLEARANCE REQUIRED</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if not stripe_link:
            st.error("Stripe checkout link is not configured.")
            return

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
            import yfinance as yf
            t = yf.Ticker(pro_ticker)
            full_hist = t.history(period="1y")
            
            try:
                info, fallback_hist = get_stock_data_func(pro_ticker, range_type="pro")
            except Exception:
                info = t.info if hasattr(t, 'info') else {}
                fallback_hist = None
            
            if full_hist is None or full_hist.empty:
                full_hist = fallback_hist

            if full_hist is not None and not full_hist.empty:
                last_date = full_hist.index.max()
                if window_selection == "90 Days":
                    filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=90))]
                elif window_selection == "180 Days":
                    filtered_hist = full_hist[full_hist.index >= (last_date - timedelta(days=180))]
                elif window_selection == "Year-To-Date (YTD)":
                    filtered_hist = full_hist[full_hist.index.year == last_date.year]
                else:
                    filtered_hist = full_hist.copy()

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
            with st.spinner("⚡ Decoding Advanced Institutional Telemetry..."):
                try:
                    url = st.secrets.get("PIPEDREAM_URL", "")
                    if url:
                        payload = {
                            "ticker": pro_ticker,
                            "tier": "pro",
                            "instructions": "Generate a comprehensive, highly detailed institutional quantitative analysis. Output strictly valid JSON. MUST include these keys with extensive paragraph-length analysis: outlook_30d, primary_support, primary_resistance, confidence_score, risk_reward_profile, macro_catalysts, institutional_order_flow, quantitative_trend_telemetry (with delta_summary and volatility_profile), contextual_intelligence, and neural_signature. Make the analysis extremely detailed and data-rich, vastly exceeding standard retail summaries."
                        }
                        res = requests.post(url, json=payload, timeout=60)
                        raw_prediction = res.json().get("prediction", "No data.") if res.status_code == 200 else "Link Failure"
                    else:
                        raw_prediction = "{'error': 'Missing API Key'}"
                    
                    # Apply Bulletproof AI Parsing!
                    json_obj, clean_output = sanitize_json_response(raw_prediction)
                    
                    if isinstance(json_obj, dict):
                        # Use robust extraction instead of relying on specific strict nesting
                        verdict, v_color = get_final_verdict(json_obj, clean_output)
                        
                        # Premium UI Banner
                        st.markdown(f"""
                        <style>
                            .pro-verdict-banner {{
                                display: flex; justify-content: space-between; align-items: center; 
                                background: linear-gradient(90deg, #05070a 0%, #0a0e17 100%);
                                border-left: 4px solid {v_color}; padding: 15px 20px; 
                                border-radius: 4px; margin-bottom: 20px;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                            }}
                            .pro-verdict-badge {{
                                border: 2px solid {v_color}; background: rgba(0,0,0,0.4); 
                                padding: 8px 24px; border-radius: 4px; font-weight: 900; 
                                color: {v_color}; font-size: 1.4rem; letter-spacing: 0.15em; 
                                box-shadow: 0 0 20px {v_color}60; text-transform: uppercase;
                            }}
                        </style>
                        <div class="pro-verdict-banner">
                            <div>
                                <h2 style="margin: 0; color: #fff; font-family: 'Courier New', monospace;">🧠 NEURAL SYNTHESIS</h2>
                                <div style="color: #8892b0; font-size: 0.9rem; margin-top: 5px;">INSTITUTIONAL GRADE ANALYSIS :: {pro_ticker.upper()}</div>
                            </div>
                            <div class="pro-verdict-badge">{verdict}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        outlook = safe_extract(json_obj, ["outlook_30d", "outlook", "trajectory", "forecast"], "Neutral")
                        if "bull" in str(outlook).lower() or "up" in str(outlook).lower() or "positive" in str(outlook).lower():
                            st.success(f"**30-Day Trajectory (Institutional Forecast):** {outlook} 🚀")
                        elif "bear" in str(outlook).lower() or "down" in str(outlook).lower() or "negative" in str(outlook).lower():
                            st.error(f"**30-Day Trajectory (Institutional Forecast):** {outlook} 🔻")
                        else:
                            st.warning(f"**30-Day Trajectory (Institutional Forecast):** {outlook} ⚖️")
                            
                        # Robust extractions for metrics
                        primary_support = safe_extract(json_obj, ["primary_support", "support", "support_level", "floor"], "N/A")
                        primary_resistance = safe_extract(json_obj, ["primary_resistance", "resistance", "resistance_level", "ceiling"], "N/A")
                        conf = safe_extract(json_obj, ["confidence_score", "confidence", "probability"], "N/A")
                        risk_reward = safe_extract(json_obj, ["risk_reward_profile", "risk_reward", "ratio"], "N/A")
                        
                        st.markdown("### 🎛️ KEY MICROSTRUCTURE ZONES")
                        c1, c2, c3, c4 = st.columns(4)
                        
                        sup_display = f"${primary_support}" if str(primary_support).replace('.','',1).isdigit() else str(primary_support)
                        res_display = f"${primary_resistance}" if str(primary_resistance).replace('.','',1).isdigit() else str(primary_resistance)
                        conf_display = f"{conf}%" if str(conf).replace('.','',1).isdigit() else str(conf)
                        
                        c1.metric("🛡️ Primary Support", sup_display)
                        c2.metric("🎯 Primary Resistance", res_display)
                        c3.metric("🤖 AI Confidence", conf_display)
                        c4.metric("⚖️ Risk/Reward", str(risk_reward).title())
                        
                        # Visual representation of AI Confidence
                        if str(conf).replace('.', '', 1).isdigit():
                            st.progress(float(conf) / 100.0, text="Neural Model Confidence Matrix")
                        
                        st.divider()
                        
                        # Extra detailed extractions for deep analysis
                        delta = safe_extract(json_obj, ["delta_summary", "trend", "price_action", "technical_analysis"], "No delta summary available.")
                        vol = safe_extract(json_obj, ["volatility_profile", "volatility", "risk_profile"], "No volatility profile available.")
                        macro = safe_extract(json_obj, ["macro_catalysts", "macro_environment", "macro"], "No macro catalysts provided.")
                        order_flow = safe_extract(json_obj, ["institutional_order_flow", "order_flow", "dark_pool"], "No institutional flow data available.")
                        context = safe_extract(json_obj, ["contextual_intelligence", "context", "news", "fundamentals"], "No contextual intelligence available.")
                        sig = safe_extract(json_obj, ["neural_signature", "signature", "model_id"], "QUANT-MATRIX-PRO-v3.0")
                        
                        st.markdown(f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px;">
    <div style="background: #0a0e17; border: 1px solid #1e293b; padding: 20px; border-radius: 6px;">
        <div style="color: #00e5ff; font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">📊 Quantitative Trend & Delta</div>
        <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">{cyber_highlight(str(delta))}</div>
        
        <div style="color: #ffaa00; font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">⚠️ Volatility & Risk Profile</div>
        <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">{cyber_highlight(str(vol))}</div>
    </div>
    
    <div style="background: #0a0e17; border: 1px solid #1e293b; padding: 20px; border-radius: 6px;">
        <div style="color: #00ff88; font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">🏦 Institutional Order Flow</div>
        <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">{cyber_highlight(str(order_flow))}</div>
        
        <div style="color: #b088ff; font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">🌍 Macro Catalysts</div>
        <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">{cyber_highlight(str(macro))}</div>
    </div>
</div>

<div style="background: #0a0e17; border: 1px solid #1e293b; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
    <div style="color: #ccd6f6; font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">🌐 Contextual Intelligence & Synthesis</div>
    <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">{cyber_highlight(str(context))}</div>
</div>
""", unsafe_allow_html=True)
                        
                        st.caption(f"**EXECUTION SIGNATURE:** `{sig}`")
                        
                        with st.expander("Show Raw Telemetry Tree"):
                            st.json(json_obj)
                    else:
                        # Fallback for completely failed JSON extraction
                        verdict, v_color = get_final_verdict(None, clean_output)
                        st.markdown(f"""
                        <style>
                            .pro-verdict-banner {{
                                display: flex; justify-content: space-between; align-items: center; 
                                background: linear-gradient(90deg, #05070a 0%, #0a0e17 100%);
                                border-left: 4px solid {v_color}; padding: 15px 20px; 
                                border-radius: 4px; margin-bottom: 20px;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                            }}
                            .pro-verdict-badge {{
                                border: 2px solid {v_color}; background: rgba(0,0,0,0.4); 
                                padding: 8px 24px; border-radius: 4px; font-weight: 900; 
                                color: {v_color}; font-size: 1.4rem; letter-spacing: 0.15em; 
                                box-shadow: 0 0 20px {v_color}60; text-transform: uppercase;
                            }}
                        </style>
                        <div class="pro-verdict-banner">
                            <div>
                                <h2 style="margin: 0; color: #fff; font-family: 'Courier New', monospace;">🧠 NEURAL SYNTHESIS</h2>
                                <div style="color: #8892b0; font-size: 0.9rem; margin-top: 5px;">INSTITUTIONAL GRADE ANALYSIS :: {pro_ticker.upper()}</div>
                            </div>
                            <div class="pro-verdict-badge">{verdict}</div>
                        </div>
                        <div style='background: #0a0e17; border: 1px solid #1e293b; padding: 25px; border-radius: 6px; color: #e2e8f0; font-family: \"Courier New\", monospace; white-space: pre-wrap; line-height: 1.7; font-size: 1.05rem; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
                            {cyber_highlight(clean_output)}
                        </div>
                        """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Pipeline error: {e}")
