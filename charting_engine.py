import streamlit as st
import requests
import re
import ast

# Graceful Plotly Import Failsafe
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def render_charting_engine(is_premium, get_stock_data_func):
    st.title("ADVANCED CANDLESTICK ENGINE")
    
    # If Plotly is missing, show a helpful installation guide instead of crashing
    if not PLOTLY_AVAILABLE:
        st.error("🔌 MISSING DEPENDENCY: Plotly is not installed in this environment.")
        st.markdown("""
        <div style="border: 1px solid #ff3333; padding: 20px; border-radius: 10px; background: rgba(255, 51, 51, 0.05); margin-bottom: 20px;">
            <h3 style="color: #ff3333; margin-top: 0;">How to Resolve This Instantly:</h3>
            <p style="color: #8892b0;">The Candlestick Engine requires <b>Plotly</b> for interactive drawing, zooming, and annotations.</p>
            <ol style="color: #ccd6f6; line-height: 1.6;">
                <li><b>If running locally:</b> Stop your server and run this command in your terminal:
                    <pre style="background: #0a0e17; padding: 10px; border-radius: 5px; color: #00ff88;">pip install plotly</pre>
                </li>
                <li><b>If deployed on Streamlit Cloud:</b> Add <code>plotly</code> to your <code>requirements.txt</code> file in your GitHub repository:
                    <pre style="background: #0a0e17; padding: 10px; border-radius: 5px; color: #00ff88;">streamlit\nyfinance\nrequests\nplotly</pre>
                </li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Render a basic line chart fallback so they still get value in the meantime
        st.subheader("📉 Standard Fallback View (Close Price Trend)")
        ticker_fallback = st.text_input("INPUT TICKER FOR BASIC CHART:", placeholder="e.g., SPY").upper()
        if ticker_fallback:
            try:
                with st.spinner("Fetching fallback data..."):
                    _, hist = get_stock_data_func(ticker_fallback, range_type="pro")
                    if hist is None or hist.empty:
                        import yfinance as yf
                        hist = yf.Ticker(ticker_fallback).history(period="3mo")
                    
                    if hist is not None and not hist.empty:
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("⚠️ No data available.")
            except Exception as e:
                st.error(f"Fallback Error: {e}")
        return

    # 1. Inputs (Normal flow when Plotly is present)
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("INPUT TICKER FOR CHARTING:", placeholder="e.g., SPY, BTC-USD").upper()
    with col2:
        period = st.selectbox("TIME HORIZON:", ["1mo", "3mo", "6mo", "1y", "2y"])

    if ticker:
        try:
            with st.spinner(f"Acquiring {period} price history..."):
                # FIX: Fetch dynamically from yfinance FIRST using the selected period to respect the dropdown
                try:
                    import yfinance as yf
                    ticker_obj = yf.Ticker(ticker)
                    hist = ticker_obj.history(period=period)
                    # Try getting the info from the helper function, fallback to raw ticker object if missing
                    try:
                        info, _ = get_stock_data_func(ticker, range_type="pro")
                    except:
                        info = ticker_obj.info
                except Exception as yf_direct_err:
                    # Robust fallback to custom helper function if yfinance directly chokes
                    info, hist = get_stock_data_func(ticker, range_type="pro")
            
            if hist is not None and not hist.empty:
                # 2. Build the Candlestick Chart
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name=ticker,
                    increasing_line_color='#00ff88',  # Neon green for up days
                    decreasing_line_color='#ff3333'   # Neon red for down days
                )])
                
                # Style the chart to match your dark/cyber aesthetic
                fig.update_layout(
                    title=f"{ticker} Price Action ({period})",
                    yaxis_title="Price (USD)",
                    template="plotly_dark",
                    plot_bgcolor='rgba(10, 14, 23, 1)', # Matches your #0a0e17 background
                    paper_bgcolor='rgba(10, 14, 23, 1)',
                    margin=dict(l=20, r=20, t=50, b=20),
                    xaxis_rangeslider_visible=False # Turn off the bulky default slider
                )

                # 3. Handle Free vs Pro Capabilities
                if is_premium:
                    st.markdown("<h4 style='color:#00ff88;'>🔓 PRO TIER: Annotation Tools Active</h4>", unsafe_allow_html=True)
                    st.caption("Use the toolbar in the top right of the chart to draw trendlines and support zones.")
                    
                    # PRO: Unlock Plotly's native drawing tools for annotations
                    config = {
                        'modeBarButtonsToAdd': [
                            'drawline', 
                            'drawopenpath', 
                            'drawrect', 
                            'eraseshape'
                        ],
                        'displaylogo': False
                    }
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    
                    st.divider()
                    
                    # PRO: AI Pattern Analysis 
                    st.subheader("🧠 LIVE AI PATTERN RECOGNITION")
                    if st.button("RUN TECHNICAL AI ANALYSIS"):
                        with st.spinner("Scanning for technical breakouts and chart patterns..."):
                            try:
                                url = st.secrets.get("PIPEDREAM_URL", "")
                                if url:
                                    res = requests.post(url, json={"ticker": ticker, "tier": "chart_pro"}, timeout=45)
                                    if res.status_code == 200:
                                        raw_prediction = res.json().get("prediction", "No data.")
                                        st.info(f"**AI VERDICT:** {raw_prediction}")
                                    else:
                                        st.error("Server error.")
                                else:
                                    st.error("Missing API Key.")
                            except Exception as e:
                                st.error(f"Pipeline error: {e}")
                                
                else:
                    # FREE: Standard Chart without Drawing Tools
                    st.markdown("<h4 style='color:#8892b0;'>🔒 STANDARD TIER VIEW</h4>", unsafe_allow_html=True)
                    
                    # Disable drawing tools for free users
                    config = {'displaylogo': False, 'displayModeBar': False}
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    
                    st.divider()
                    
                    # Upsell block
                    st.markdown("""
                    <div style="border: 1px solid #1e293b; padding: 20px; border-radius: 10px; background: #0a0e17;">
                        <h3 style='color: #00e5ff; margin-top:0;'>Upgrade to PRO to unlock Chart Annotations & AI Pattern Analysis</h3>
                        <p style='color: #8892b0;'>Pro users can draw custom trendlines directly on the chart and trigger our Neural Link to analyze complex candlestick formations in real-time.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("UPGRADE TERMINAL ACCESS", "https://buy.stripe.com/test_eVqcN4eUHedq3J8aSDe3e00")

            else:
                st.warning("⚠️ Market data unavailable for charting.")
        except Exception as e:
            st.error(f"⚠️ CHARTING ERROR: {str(e)}")
