import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import ast

# 1. Page Configuration & Ultra-Sleek Hexagonal Styling
st.set_page_config(page_title="SOAR MARKETS", layout="wide")

st.markdown("""
    <style>
    /* 1. REGULAR HEXAGONAL BACKGROUND (Pure Black Fill, Glowing Lines) */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        /* Perfect Hexagonal Grid via SVG */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'%3E%3Cpath d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='%2300f2ff' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
        background-attachment: fixed;
        color: #ffffff;
    }

    /* 2. SIDEBAR STYLING */
    [data-testid="stSidebar"] { 
        background-color: #010408; 
        border-right: 2px solid #00f2ff;
        box-shadow: 5px 0 15px rgba(0, 242, 255, 0.2);
    }

    /* 3. GLOWING CYAN TITLES */
    h1, h2, h3 { 
        color: #00f2ff; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.6); 
        font-family: 'Courier New', monospace; 
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* 4. INTERACTIVE METRIC BOXES (Original Cyan Hover) */
    .stMetric { 
        background: rgba(0, 0, 0, 0.85) !important;
        border: 1px solid rgba(0, 242, 255, 0.3) !important;
        border-radius: 4px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        border: 1px solid #00f2ff !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
        transform: scale(1.02);
    }

    /* 5. SYNCED BLUE-CYAN GRADIENT BUTTONS */
    .stButton>button, [data-testid="stLinkButton"]>a { 
        background: linear-gradient(135deg, #00f2ff 0%, #0072ff 100%) !important; 
        color: #000000 !important; 
        font-weight: 800 !important; 
        width: 100% !important; 
        border: none !important; 
        border-radius: 2px !important;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.4) !important;
        text-decoration: none !important;
        text-align: center !important;
        display: inline-block !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover, [data-testid="stLinkButton"]>a:hover {
        filter: brightness(1.2);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.7) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Functional Data Logic (Untouched/Robust)
@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        raw_info = stock.info
    except:
        raw_info = {}
    try:
        fast_info = stock.fast_info
    except:
        fast_info = {}

    info = {
        "marketCap": raw_info.get("marketCap") or fast_info.get("marketCap") or "N/A",
        "volume": raw_info.get("regularMarketVolume") or fast_info.get("lastVolume") or "N/A",
        "fiftyTwoWeekHigh": raw_info.get("fiftyTwoWeekHigh") or fast_info.get("yearHigh") or "N/A",
        "trailingPE": raw_info.get("trailingPE") or "N/A"
    }
    hist = stock.history(period="1mo")
    return info, hist

CANDIDATE_POOL = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL", "AVGO", "META", "AMZN", "PLTR"]

@st.cache_data(ttl=600)
def get_dynamic_leaderboard(tickers):
    leaderboard = []
    try:
        data = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
        for t in tickers:
            try:
                hist = data[t]
                if len(hist) >= 2:
                    current = float(hist['Close'].iloc[-1])
                    prev = float(hist['Close'].iloc[-2])
                    delta = ((current - prev) / prev) * 100
                    leaderboard.append({"ticker": t, "price": current, "delta": delta})
            except: continue
        return sorted(leaderboard, key=lambda x: x['delta'], reverse=True)[:5]
    except: return []

# 3. Sidebar
with st.sidebar:
    st.title("SOAR CORE")
    st.subheader("TOP GAINERS")
    top_5 = get_dynamic_leaderboard(CANDIDATE_POOL)
    for item in top_5:
        st.metric(label=item["ticker"], value=f"${item['price']:.2f}", delta=f"{item['delta']:.2f}%")

    st.divider()
    st.markdown("### **LEVEL 2 CLEARANCE**\n* Unlimited Neural Dives\n* 30-Day Intelligence")
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/your_link")

# 4. Main Interface
st.title("🚀 SOAR MARKETS")

# Upgrade Button right under Title
col_main, col_btn = st.columns([3, 1])
with col_btn:
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/your_link")

ticker = st.text_input("INPUT STOCK PROTOCOL:", placeholder="e.g. NVDA").upper()

if st.button("EXECUTE NEURAL DIVE"):
    if ticker:
        try:
            info, hist = get_stock_data(ticker)
            
            with st.spinner("Decoding Neural Telemetry..."):
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    st.success("📡 NEURAL LINK ESTABLISHED")
                    with st.container(border=True):
                        raw = res.json().get("prediction", "")
                        # Decoder for AI Output
                        try:
                            if isinstance(raw, str) and "candidates" in raw:
                                data = ast.literal_eval(raw)
                                clean_text = data["candidates"][0]["content"]["parts"][0]["text"]
                            elif isinstance(raw, dict) and "candidates" in raw:
                                clean_text = raw["candidates"][0]["content"]["parts"][0]["text"]
                            else: clean_text = str(raw)
                        except: clean_text = str(raw)
                        st.markdown(clean_text)
                else: st.error("NEURAL LINK FAILURE")

            st.divider()
            
            col_chart, col_stats = st.columns([2, 1])
            with col_chart:
                st.subheader(f"📊 {ticker} TREND")
                st.line_chart(hist['Close'])

            with col_stats:
                st.subheader("📑 METRICS")
                def fmt(val, cur=True):
                    if not isinstance(val, (int, float)): return "N/A"
                    return f"${val:,.2f}" if cur else f"{val:,.0f}"
                
                st.write(f"**Market Cap:** {fmt(info['marketCap'])}")
                st.write(f"**P/E Ratio:** {info['trailingPE']}")
                st.write(f"**Volume:** {fmt(info['volume'], False)}")
                st.write(f"**52W High:** {fmt(info['fiftyTwoWeekHigh'])}")

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")
