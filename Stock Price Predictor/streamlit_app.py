"""
Streamlit Live Preview for Stock Price Predictor
"""

import time
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go

from live_predictor import LiveStockPredictor
import config

st.set_page_config(page_title="Stock Price Predictor - Live", layout="wide")

# Sidebar controls
st.sidebar.title("⚙️ Controls")
symbol = st.sidebar.selectbox("Stock Symbol", options=config.POPULAR_STOCKS, index=0)
period = st.sidebar.selectbox(
    "History Period (for training)", options=list(config.TIME_PERIODS.keys()), index=list(config.TIME_PERIODS.keys()).index("2y")
)
update_interval = st.sidebar.number_input(
    "Auto-refresh seconds", min_value=10, max_value=300, value=config.LIVE_SETTINGS.get('update_interval_seconds', 30), step=5
)

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    fetch_btn = st.button("🔄 Update Data")
with col_btn2:
    train_btn = st.button("🎯 Train Model")

# Header
st.title("📈 Live Stock Price Predictor")
st.caption("Intraday live data with next-day direction prediction")

# Predictor instance (cache per selection)
@st.cache_resource(show_spinner=False)
def get_predictor(selected_symbol: str, selected_period: str) -> LiveStockPredictor:
    return LiveStockPredictor(symbol=selected_symbol, period=selected_period, update_interval=update_interval)

predictor = get_predictor(symbol, period)

# Update or train actions
if fetch_btn:
    with st.spinner("Fetching historical data and creating features..."):
        predictor.fetch_data()
        predictor.create_features()

if train_btn:
    with st.spinner("Training model..."):
        if predictor.features is None:
            predictor.fetch_data()
            predictor.create_features()
        predictor.train_model()

# Ensure we have data
if predictor.data is None:
    predictor.fetch_data()
    predictor.create_features()

# Live prediction section
live_col1, live_col2, live_col3 = st.columns(3)

with live_col1:
    pred = predictor.get_live_prediction()
    if pred:
        st.metric(label="Prediction", value=pred['direction'], delta=f"{pred['confidence']:.1f}% confidence")
    else:
        st.info("Train the model to see predictions.")

with live_col2:
    current_price = predictor.get_current_price()
    price_change = predictor.get_price_change()
    if current_price is not None:
        delta_str = f"{price_change:.2f}%" if price_change is not None else None
        st.metric(label=f"{symbol} Price", value=f"${current_price:.2f}", delta=delta_str)
    else:
        st.warning("No live price yet")

with live_col3:
    if predictor.model is not None:
        st.success("Model: Trained")
    else:
        st.error("Model: Not trained")

# Chart
fig = predictor.create_live_chart()
st.plotly_chart(fig, use_container_width=True)

# Footer info
st.caption(
    f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Interval: {config.LIVE_SETTINGS.get('intraday_interval', '1m')} • Auto-refresh: {update_interval}s"
)

