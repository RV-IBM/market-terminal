import streamlit as st
import requests
import json
import ast
import re

# Premium cyber-themed word highlighting engine
def cyber_highlight(text):
    if not isinstance(text, str):
        return text
    # Map key positive terms to neon green, negative terms to neon red
    positives = r"\b(bullish|support|breakout|growth|gains|rebound|upside|accumulate|momentum|long|strength|buy)\b"
    negatives = r"\b(bearish|resistance|drawdown|drop|fall|decline|downside|sell|risk|weakness|contraction|short|losses)\b"
    
    text = re.sub(positives, r"<span style='color:#00ff88; font-weight:bold; text-shadow:0 0 5px rgba(0,255,136,0.3);'>\1</span>", text, flags=re.IGNORECASE)
    text = re.sub(negatives, r"<span style='color:#ff3333; font-weight:bold; text-shadow:0 0 5px rgba(255,51,51,0.3);'>\1</span>", text, flags=re.IGNORECASE)
    return text

def render_free_terminal(get_stock_data_func):
    st.title("STANDARD INTELLIGENCE STREAM")
    
    ticker = st.text_input("INPUT STOCK PROTOCOL (FREE TIER):", placeholder="e.g., NVDA, AAPL, TSLA").upper()
    
    if ticker:
        # FIX: Fetch live market data safely OUTSIDE the button click scope!
        try:
            with st.spinner("Establishing secure telemetry..."):
                info, hist = get_stock_data_func(ticker, range_type="free")
        except Exception as e:
            st.error(f"TELEMETRY OFFLINE: {e}")
            return
            
        if info is None or hist is None or hist.empty:
            st.warning(f"Live telemetry for {ticker} is temporarily unavailable.")
            return

        # 1. LIVE DATA PREPARATION
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or hist['Close'].iloc[-1]
        prev_close = info.get("previousClose") or hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        price_change = current_price - prev_close
        pct_change = (price_change / prev_close) * 100 if prev_close else 0.0
        
        market_cap = info.get("marketCap", "N/A")
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
        
        day_high = info.get("dayHigh", current_price)
        day_low = info.get("dayLow", current_price)
        volume = info.get("volume", 0)
        
        # 52-week trajectory calculation
        low_52w = info.get("fiftyTwoWeekLow", current_price)
        high_52w = info.get("fiftyTwoWeekHigh", current_price)
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

        st.subheader("STANDARD TELEMETRY STREAM")
        
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
        st.subheader(f"{ticker} 30-DAY PRICE PATH")
        st.line_chart(hist['Close'])

        st.divider()

        # 3. TRIGGER NEURAL NETWORK ANALYSIS
        if st.button("RUN STANDARD NEURAL VERDICT"):
            # Prepare fast telemetry payload
            payload = {
                "ticker": ticker,
                "tier": "free",
                "current_price": current_price,
                "pct_change": pct_change,
                "momentum": momentum_state
            }
            
            with st.spinner("Connecting to neural processor..."):
                try:
                    url = st.secrets.get("PIPEDREAM_URL")
                    if not url:
                        st.error("CONFIGURATION REQUIRED: PIPEDREAM_URL key is missing from secrets.")
                        return
                        
                    res = requests.post(url, json=payload, timeout=60)
                    
                    if res.status_code == 200:
                        st.success("NEURAL LINK ESTABLISHED")
                        raw_prediction = res.json().get("prediction", "No telemetry data.")
                        
                        # Strip thinking tags if models outputs them
                        clean_output = str(raw_prediction)
                        clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
                        
                        # Handle serialization formatting issues
                        if clean_output.startswith("```json"):
                            clean_output = clean_output.replace("```json", "").replace("```", "").strip()
                            
                        parsed_dict = None
                        try:
                            parsed_dict = json.loads(clean_output)
                        except:
                            try:
                                parsed_dict = ast.literal_eval(clean_output)
                            except:
                                parsed_dict = None

                        # Pull out Outlook & Support safely, providing computed fallbacks
                        if isinstance(parsed_dict, dict):
                            # Try multiple key variants in case AI generates unique keys
                            outlook = parsed_dict.get("Outlook", parsed_dict.get("30-Day Outlook", parsed_dict.get("outlook", "Neutral")))
                            support = parsed_dict.get("Support", parsed_dict.get("support_levels", parsed_dict.get("support", "N/A")))
                            resistance = parsed_dict.get("Resistance", parsed_dict.get("resistance", "N/A"))
                            summary = parsed_dict.get("Contextual Intelligence", parsed_dict.get("analysis", parsed_dict.get("summary", "")))
                        else:
                            # Failsafe Fallback if AI printed non-JSON markdown paragraphs
                            outlook = "Active" if pct_change > 0 else "Consolidating"
                            support = f"${day_low:.2f}"
                            resistance = f"${day_high:.2f}"
                            summary = clean_output

                        # Render Cyberized Intelligence Box
                        outlook_color = "#00ff88" if "bull" in outlook.lower() or "up" in outlook.lower() else "#ff3333" if "bear" in outlook.lower() or "down" in outlook.lower() else "#00e5ff"
                        
                        # Apply keyword highlights to the summary narrative
                        highlighted_summary = cyber_highlight(summary) if summary else f"Asset price is hovering in its short-term trading bounds. Active levels suggest consolidation around its 52-week trajectory midpoint."

                        html_code = (
                            f'<div style="background-color:#08101e; border: 1px solid #00e5ff; border-radius:10px; padding:25px; box-shadow:0 0 15px rgba(0,229,255,0.15); margin-top:15px;">'
                            f'<h3 style="color:#00e5ff; margin-top:0; font-family:\'Courier New\', monospace; letter-spacing:0.1em; text-shadow:0 0 10px rgba(0,229,255,0.5);">NEURAL INTEGRATION PROTOCOL</h3>'
                            f'<div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:20px;">'
                            f'<div style="border-left: 3px solid {outlook_color}; background:rgba(30,41,59,0.5); padding:10px 15px; border-radius:0 6px 6px 0; min-width:120px;">'
                            f'<div class="metric-label" style="font-size:0.7rem; color:#8892b0; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Forecast Outlook</div>'
                            f'<div style="font-size:1.1rem; font-weight:bold; color:{outlook_color};">{outlook}</div>'
                            f'</div>'
                            f'<div style="border-left: 3px solid #00ff88; background:rgba(30,41,59,0.5); padding:10px 15px; border-radius:0 6px 6px 0; min-width:120px;">'
                            f'<div class="metric-label" style="font-size:0.7rem; color:#8892b0; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Expected Support</div>'
                            f'<div style="font-size:1.1rem; font-weight:bold; color:#00ff88; font-family: monospace;">{support}</div>'
                            f'</div>'
                            f'<div style="border-left: 3px solid #ff3333; background:rgba(30,41,59,0.5); padding:10px 15px; border-radius:0 6px 6px 0; min-width:120px;">'
                            f'<div class="metric-label" style="font-size:0.7rem; color:#8892b0; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Target Resistance</div>'
                            f'<div style="font-size:1.1rem; font-weight:bold; color:#ff3333; font-family: monospace;">{resistance}</div>'
                            f'</div>'
                            f'</div>'
                            f'<div style="border-top:1px solid #1e293b; padding-top:15px;">'
                            f'<h4 style="color:#ccd6f6; margin-top:0; font-size:0.95rem;">PERFORMANCE & MOMENTUM SUMMARY</h4>'
                            f'<p style="color:#8892b0; font-size:0.9rem; line-height:1.6; margin-bottom:0;">{highlighted_summary}</p>'
                            f'</div>'
                            f'</div>'
                        )
                        st.markdown(html_code, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"NEURAL LINK FAILURE: Server returned status {res.status_code}")
                except requests.exceptions.Timeout:
                    st.warning("TELEMETRY DELAY: Server took too long to compile the neural report. Please re-trigger the link.")
                except requests.exceptions.RequestException as e:
                    st.error(f"PIPELINE ERROR: Interface gateway disconnected. Details: {e}")
