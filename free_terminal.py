import streamlit as st
import requests
import ast

def render_free_terminal(get_stock_data_func):
    st.title("STANDARD INTELLIGENCE STREAM")
    ticker = st.text_input("INPUT STOCK PROTOCOL (FREE TIER):", placeholder="e.g., NVDA, AMD").upper()

        # ====================================================================
    # BASE NEURAL VERDICT SECTION (For Free/Standard Tier)
    # ====================================================================
    st.divider()
    
    # NOTE: Ensure 'ticker' matches your free script's input variable!
    if st.button("RUN STANDARD NEURAL VERDICT"):
        if ticker:
            try:
                info, hist = get_stock_data_func(ticker, range_type="free")
                
                with st.spinner("Decoding Standard Quant Telemetry..."):
                    url = st.secrets["PIPEDREAM_URL"]
                    
                    try:
                        res = requests.post(url, json={"ticker": ticker, "tier": "free"}, timeout=45)
                        
                        if res.status_code == 200:
                            st.success("⚡ STANDARD LEVEL NEURAL LINK ESTABLISHED")
                            with st.container(border=True):
                                
                                # 1. Catch raw response safely
                                try:
                                    resp_data = res.json()
                                    if isinstance(resp_data, dict):
                                        raw_prediction = resp_data.get("prediction", resp_data)
                                    else:
                                        raw_prediction = str(resp_data)
                                except:
                                    raw_prediction = res.text
                                
                                                              
                                # 2. Drill down and extract the text payload safely
                                # 2. Drill down and extract the text payload safely
                                clean_output = ""
                                
                                # 2. Drill down and extract the text payload safely
                                try:
                                    import json
                                    import ast
                                    
                                    # Convert stringified JSON into a real dictionary
                                    if isinstance(raw_prediction, str):
                                        clean_str = raw_prediction.strip()
                                        if clean_str.startswith("```json"):
                                            clean_str = clean_str[7:-3]
                                        elif clean_str.startswith("```"):
                                            clean_str = clean_str[3:-3]
                                        clean_str = clean_str.strip()
                                        
                                        try:
                                            parsed_dict = json.loads(clean_str)
                                        except:
                                            try:
                                                parsed_dict = ast.literal_eval(clean_str)
                                            except:
                                                parsed_dict = raw_prediction
                                    else:
                                        parsed_dict = raw_prediction
    
                                    # Extract inner text if wrapped in Gemini candidate structure
                                    if isinstance(parsed_dict, dict):
                                        if "candidates" in parsed_dict and len(parsed_dict["candidates"]) > 0:
                                            candidate = parsed_dict["candidates"][0]
                                            if "content" in candidate and "parts" in candidate["content"]:
                                                clean_output = candidate["content"]["parts"][0]["text"]
                                            elif "text" in candidate:
                                                clean_output = candidate["text"]
                                            else:
                                                clean_output = parsed_dict.get("text", str(parsed_dict))
                                        else:
                                            clean_output = parsed_dict.get("text", parsed_dict.get("output", str(raw_prediction)))
                                    else:
                                        clean_output = str(raw_prediction)
                                        
                                except Exception as e:
                                    clean_output = str(raw_prediction)
    
                                # 3. Final visual formatting
                                if isinstance(clean_output, str):
                                    clean_output = clean_output.replace("\\n", "\n").replace("\\\"", "\"")
                                    
                                    # Scrub out <think> tags from reasoning models
                                    import re
                                    clean_output = re.sub(r'<think>.*?</think>', '', clean_output, flags=re.DOTALL).strip()
                                    
                                    # --- NEW: SMART JSON DETECTOR ---
                                    # If the AI returned pure JSON text, render it as a clean UI block
                                    if clean_output.startswith("{") and clean_output.endswith("}"):
                                        try:
                                            json_obj = json.loads(clean_output)
                                            st.json(json_obj) # This makes it beautifully color-coded and collapsible
                                        except:
                                            st.markdown(f"```json\n{clean_output}\n```")
                                    else:
                                        st.markdown(clean_output)
                                else:
                                    st.write(clean_output)
                                    
                        else:
                            st.error(f"NEURAL LINK FAILURE: Server returned status {res.status_code}")
                            
                    except requests.exceptions.Timeout:
                        st.warning("🦤 TELEMETRY DELAY: Matrix generation took longer than 45 seconds. Please click again to retry.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"⚠️ PIPELINE ERROR: Interface gateway disconnected. Details: {e}")
                    
                # ==========================================================
                # RESTORED: THE CHART AND STATS RENDERING!
                # ==========================================================
                st.divider()
                
                if hist is not None and not hist.empty:
                    col_chart, col_stats = st.columns([2, 1])
                    
                    with col_chart:
                        st.subheader(f"📊 {ticker.upper()} 30-DAY TREND")
                        st.line_chart(hist['Close'])
                        
                    with col_stats:
                        st.subheader("📄 KEY METRICS")
                        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                        st.write(f"**Volume:** {info.get('volume', 'N/A')}")
                        st.write(f"**52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
                else:
                    st.warning(f"⚠️ SYSTEM NOTIFICATION: Live telemetry for {ticker} is temporarily unavailable.")
                    
            except Exception as e:
                st.error(f"SYSTEM CRASH: {str(e)}")
        else:
            st.warning("PLEASE INPUT A TICKER.")
