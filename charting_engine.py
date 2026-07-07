import streamlit as st
import plotly.graph_objects as go
import requests
import re
import ast

def render_charting_engine(is_premium, get_stock_data_func):
    st.title("ADVANCED CANDLESTICK ENGINE")
    
    # 1. Inputs
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("INPUT TICKER FOR CHARTING:", placeholder="e.g., SPY, BTC-USD").upper()
    with col2:
        period = st.selectbox("TIME HORIZON:", ["1mo", "3mo", "6mo", "1y", "2y"])

    if ticker:
        try:
            with st.spinner("Fetching market data..."):
                # Fetch data using your existing helper function
                info, hist = get_stock_data_func(ticker, range_type="pro")
                
                # Fallback if get_stock_data_func has issues
                if hist is None or hist.empty:
                    import yfinance as yf
                    hist = yf.Ticker(ticker).history(period=period)
            
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
                    st.subheader("LIVE AI PATTERN RECOGNITION")
                    if st.button("RUN TECHNICAL AI ANALYSIS"):
                        with st.spinner("Scanning for technical breakouts and chart patterns..."):
                            try:
                                url = st.secrets.get("PIPEDREAM_URL", "")
                                if url:
                                    # We send tier="chart_pro" so your Pipedream workflow knows to look at technicals
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
                st.warning("Market data unavailable for charting.")
        except Exception as e:
            st.error(f"⚠️ CHARTING ERROR: {str(e)}")
