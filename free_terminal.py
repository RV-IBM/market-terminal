import streamlit as st
import requests
import json
import ast
import re

def sanitize_json_response(raw_text):
    """Strips reasoning/thinking tags and parses JSON from raw backend response."""
    clean_text = re.sub(r'<think>.*?</think>', '', str(raw_text), flags=re.DOTALL).strip()
    
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
            
    if "{" in clean_text and "}" in clean_text:
        try:
            start = clean_text.find("{")
            end = clean_text.rfind("}") + 1
            json_substr = clean_text[start:end]
            try:
                return json.loads(json_substr), clean_text
            except Exception:
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

# Premium cyber-themed word highlighting engine
def cyber_highlight(text):
    if not isinstance(text, str):
        return text
    # Map key positive terms to neon green, negative terms to neon red
    positives = r"\b(bullish|support|breakout|growth|gains|rebound|upside|accumulate|momentum|long|strength|buy)\b"
    negatives = r"\b(bearish|resistance|drawdown|drop|fall|decline|downside|sell|risk|weakness|contraction|short|losses)\b"
    
    # Removed text-shadow to keep the text clean and readable without the glowing effect
    text = re.sub(positives, r"<span style='color:#00ff88; font-weight:bold;'>\1</span>", text, flags=re.IGNORECASE)
    text = re.sub(negatives, r"<span style='color:#ff3333; font-weight:bold;'>\1</span>", text, flags=re.IGNORECASE)
    return text

def safe_extract(data_obj, possible_keys, default="N/A"):
    """Recursively and aggressively searches a dictionary/list for fuzzy key matches."""
    if isinstance(data_obj, dict):
        # 1. Exact match checking
        for k in possible_keys:
            if k in data_obj and data_obj[k] not in [None, "", "N/A", "null", []]:
                val = data_obj[k]
                if isinstance(val, list) and len(val) > 0: return val[0]
                if not isinstance(val, (dict, list)): return val
        
        # 2. Fuzzy key match (substring)
        for k, v in data_obj.items():
            k_lower = str(k).lower()
            for pk in possible_keys:
                if pk.lower() in k_lower and v not in [None, "", "N/A", "null", []]:
                    if isinstance(v, list) and len(v) > 0:
                        if not isinstance(v[0], (dict, list)): return v[0]
                    elif not isinstance(v, (dict, list)): 
                        return v
                        
        # 3. Recursive search in values
        for v in data_obj.values():
            res = safe_extract(v, possible_keys, None)
            if res is not None: return res
            
    elif isinstance(data_obj, list):
        # Recurse into lists
        for item in data_obj:
            res = safe_extract(item, possible_keys, None)
            if res is not None: return res
            
    return default

def render_free_terminal(get_stock_data_func):
    st.title("STANDARD INTELLIGENCE STREAM")
    
    ticker = st.text_input("INPUT STOCK PROTOCOL (FREE TIER):", placeholder="e.g., NVDA, AAPL, TSLA").upper()
    
    if ticker:
        # FIX: Fetch live market data safely OUTSIDE the button click scope!
        try:
            with st.spinner("Establishing secure telemetry..."):
                info, hist = get_stock_data_func(ticker, range_type="free")
        except Exception as e:
            st.error(f"⚠️ TELEMETRY OFFLINE: {e}")
            return
            
        if info is None or hist is None or hist.empty:
            st.warning(f"⚠️ Live telemetry for {ticker} is temporarily unavailable.")
            return

        # 1. LIVE DATA PREPARATION
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or hist['Close'].iloc[-1]
        prev_close = info.get("previousClose") or hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        price_change = current_price - prev_close
        pct_change = (price_change / prev_close) * 100 if prev_close else 0.0
        
        market_cap = info.get("marketCap") or info.get("totalAssets", "N/A")
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1e12:
                market_cap_str = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                market_cap_str = f"${market_cap/1e9:.2f}B"
            else:
                market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = "N/A"
            
        pe_ratio = info.get("trailingPE") or info.get("forwardPE") or "N/A"
        pe_ratio_str = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
        
        day_high = info.get("dayHigh") or hist['High'].iloc[-1]
        day_low = info.get("dayLow") or hist['Low'].iloc[-1]
        volume = info.get("volume") or hist['Volume'].iloc[-1]
        
        # 52-week trajectory calculation
        low_52w = info.get("fiftyTwoWeekLow") or hist['Low'].min()
        high_52w = info.get("fiftyTwoWeekHigh") or hist['High'].max()
        range_52w = high_52w - low_52w
        position_52w = ((current_price - low_52w) / range_52w * 100) if range_52w else 50.0

        # Algorithmic Momentum State Determination
        if pct_change > 1.5:
            momentum_state = "Bullish breakout momentum"
        elif pct_change < -1.5:
            momentum_state = "Bearish distribution pressure"
        else:
            momentum_state = "Consolidating neutral range"

        st.divider()

        # 2. RENDER LIVE TELEMETRY DECK
        change_color = "#00ff88" if price_change >= 0 else "#ff3333"
        change_sign = "+" if price_change >= 0 else ""

        # UI Styling Injector
        st.markdown(f"""
        <style>
            .cyber-card {{
                background-color: #0a0e17;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 18px;
                margin-bottom: 15px;
                box-shadow: 0 4px 20px rgba(0, 229, 255, 0.05);
            }}
            .metric-label {{
                color: #8892b0;
                font-size: 0.85rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 4px;
            }}
            .metric-value {{
                color: #ccd6f6;
                font-size: 1.4rem;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }}
            .pulse-bar {{
                height: 6px;
                background: #1e293b;
                border-radius: 3px;
                overflow: hidden;
                margin-top: 8px;
            }}
            .pulse-fill {{
                height: 100%;
                background: linear-gradient(90deg, #00e5ff, #00ff88);
                border-radius: 3px;
            }}
        </style>
        """, unsafe_allow_html=True)

        st.subheader("📊 STANDARD TELEMETRY STREAM")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="cyber-card">
                <div class="metric-label">Last Price</div>
                <div class="metric-value" style="color: {change_color};">${current_price:.2f}</div>
                <div style="font-size:0.8rem; color:{change_color}; font-weight:bold;">
                    {change_sign}{price_change:.2f} ({change_sign}{pct_change:.2f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m2:
            st.markdown(f"""
            <div class="cyber-card">
                <div class="metric-label">Market Capitalization</div>
                <div class="metric-value">{market_cap_str}</div>
                <div style="font-size:0.8rem; color:#8892b0;">Valuation Class</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m3:
            st.markdown(f"""
            <div class="cyber-card">
                <div class="metric-label">P/E Multiple</div>
                <div class="metric-value">{pe_ratio_str}</div>
                <div style="font-size:0.8rem; color:#8892b0;">Trailing earnings</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m4:
            st.markdown(f"""
            <div class="cyber-card">
                <div class="metric-label">Daily Volatility</div>
                <div class="metric-value">${day_high-day_low:.2f}</div>
                <div style="font-size:0.8rem; color:#8892b0;">Spread Low to High</div>
            </div>
            """, unsafe_allow_html=True)

        # 52-Week Trajectory Bar
        st.markdown(f"""
        <div class="cyber-card" style="padding-top: 10px; padding-bottom: 15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="metric-label" style="margin-bottom:0;">52-Week Range Position</span>
                <span style="font-size:0.8rem; color:#00e5ff; font-family: monospace;">{position_52w:.1f}% Percentile</span>
            </div>
            <div class="pulse-bar">
                <div class="pulse-fill" style="width: {min(max(position_52w, 0.0), 100.0)}%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#8892b0; margin-top:5px; font-family: monospace;">
                <span>52W Low: ${low_52w:.2f}</span>
                <span>52W High: ${high_52w:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Basic historical line chart (shows up automatically without needing button click)
        st.subheader(f"📈 {ticker} 30-DAY PRICE PATH")
        st.line_chart(hist['Close'])

        st.divider()

        # 3. TRIGGER NEURAL NETWORK ANALYSIS
        if st.button("RUN STANDARD NEURAL VERDICT"):
            # Prepare fast telemetry payload with explicit rating instructions
            payload = {
                "ticker": ticker,
                "tier": "free",
                "current_price": current_price,
                "pct_change": pct_change,
                "momentum": momentum_state,
                "instructions": "Conclude your analysis with a clear rating of exactly BUY, HOLD, or SELL. Output MUST be valid JSON."
            }
            
            with st.spinner("⚡ Connecting to neural processor..."):
                try:
                    url = st.secrets.get("PIPEDREAM_URL")
                    if not url:
                        st.error("🔑 CONFIGURATION REQUIRED: PIPEDREAM_URL key is missing from secrets.")
                        return
                        
                    res = requests.post(url, json=payload, timeout=60)
                    
                    if res.status_code == 200:
                        st.success("⚡ NEURAL LINK ESTABLISHED")
                        raw_prediction = res.json().get("prediction", "No telemetry data.")
                        
                        clean_output = str(raw_prediction)
                        
                        if isinstance(clean_output, str):
                            clean_output = clean_output.replace("\\n", "\n").replace("\\\"", "\"")
                            
                            # Scrub out <think> tags from reasoning models
                            import re
                            clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
                            
                            # Strip Markdown formatting (code blocks)
                            if "```json" in clean_output.lower():
                                try: clean_output = clean_output.split(re.search(r'```json', clean_output, re.IGNORECASE).group())[1].split("```")[0].strip()
                                except: pass
                            elif "```" in clean_output:
                                try: clean_output = clean_output.split("```")[1].split("```")[0].strip()
                                except: pass
                                
                            # Isolate JSON block if there's conversational text wrapping it
                            json_match = re.search(r'\{.*\}', clean_output, re.DOTALL)
                            if json_match:
                                clean_output = json_match.group(0)
                            
                            # --- SMART JSON DETECTOR & PREMIUM DASHBOARD ---
                            if clean_output.startswith("{") and clean_output.endswith("}"):
                                try:
                                    import json
                                    json_obj = json.loads(clean_output)
                                    
                                    # If Pipedream returned JSON, try to extract rich data safely
                                    if isinstance(json_obj, dict):
                                        # Extract the final verdict
                                        verdict, v_color = get_final_verdict(json_obj, clean_output)
                                        
                                        st.markdown(f"""
                                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                                            <h3 style="margin: 0;">🧠 Neural Analysis: {ticker.upper()}</h3>
                                            <div style="border: 2px solid {v_color}; background: rgba(0,0,0,0.3); padding: 6px 16px; border-radius: 6px; font-weight: bold; color: {v_color}; font-size: 1.2rem; letter-spacing: 0.1em; box-shadow: 0 0 12px {v_color}40;">
                                                {verdict}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Dynamic Robust Extractors
                                        outlook = safe_extract(json_obj, ["outlook_30d", "outlook", "trajectory", "forecast", "prediction", "trend"], "Neutral")
                                        if "Bullish" in str(outlook) or "up" in str(outlook).lower():
                                            st.success(f"**30-Day Outlook:** {outlook} 🚀")
                                        elif "Bearish" in str(outlook) or "down" in str(outlook).lower():
                                            st.error(f"**30-Day Outlook:** {outlook} 🔻")
                                        else:
                                            st.warning(f"**30-Day Outlook:** {outlook} ⚖️")
                                        
                                        support_val = safe_extract(json_obj, ["primary_support", "support_level", "support", "support_1", "floor"], "N/A")
                                        resistance_val = safe_extract(json_obj, ["primary_resistance", "resistance_level", "resistance", "resistance_1", "ceiling", "target"], "N/A")
                                        confidence_val = safe_extract(json_obj, ["confidence_score", "confidence", "ai_confidence", "probability", "score"], "N/A")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        
                                        sup_display = f"${support_val}" if str(support_val).replace('.','',1).isdigit() else str(support_val)
                                        res_display = f"${resistance_val}" if str(resistance_val).replace('.','',1).isdigit() else str(resistance_val)
                                        conf_display = f"{confidence_val}%" if str(confidence_val).replace('.','',1).isdigit() else str(confidence_val)

                                        col1.metric("🛡️ Primary Support", sup_display)
                                        col2.metric("🎯 Primary Resistance", res_display)
                                        col3.metric("🤖 AI Confidence", conf_display)
                                        
                                        # Detailed Expandable Sections
                                        delta_sum = safe_extract(json_obj, ["delta_summary", "summary", "trend_analysis", "analysis", "reasoning"], "Trend analysis complete.")
                                        vol_profile = safe_extract(json_obj, ["volatility_profile", "volatility", "risk_profile", "risk", "beta"], "Standard market conditions detected.")
                                        context = safe_extract(json_obj, ["contextual_intelligence", "context", "market_context", "fundamental", "news"], "No additional context provided.")
                                        signature = safe_extract(json_obj, ["neural_signature", "signature", "model_id", "model"], "QUANT-MATRIX-v2.5")

                                        with st.expander("📊 Quantitative Trend Telemetry", expanded=True):
                                            st.markdown("**Delta Summary**")
                                            st.info(delta_sum)
                                            st.markdown("**Volatility Profile**")
                                            st.warning(vol_profile)
                                            
                                        with st.expander("🌐 Contextual Intelligence", expanded=True):
                                            st.write(context)
                                            
                                        st.caption(f"Neural Signature: `{signature}`")
                                    else:
                                        st.json(json_obj)
                                except Exception as e:
                                    # Fallback rendering if JSON parsing fails mid-way
                                    st.markdown(f"<div class='cyber-card'>{cyber_highlight(clean_output)}</div>", unsafe_allow_html=True)
                            else:
                                # Fallback rendering for raw text responses
                                st.markdown(f"<div class='cyber-card'>{cyber_highlight(clean_output)}</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"NEURAL LINK FAILURE: Server returned status {res.status_code}")
                        
                except requests.exceptions.Timeout:
                    st.warning("🦤 TELEMETRY DELAY: Matrix generation took longer than 60 seconds.")
                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ PIPELINE ERROR: Interface gateway disconnected. Details: {e}")
