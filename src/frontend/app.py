import streamlit as st
import pandas as pd
from components.charts import plot_predictions, plot_volatility
from components.metrics import display_metrics
from utils.api_client import APIClient


st.set_page_config(
    page_title="BrechApp",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 BrechApp - Cryptocurrency Analysis")

api_client = APIClient()

with st.sidebar:
    st.header("Configuration")
    symbol = st.text_input("Symbol", value="BTC-USD")
    model = st.selectbox("Model", ["arima", "prophet", "garch"])
    horizon = st.slider("Prediction Horizon (days)", 7, 90, 30)
    
    if st.button("Run Analysis"):
        st.session_state.run_analysis = True

if st.session_state.get('run_analysis', False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Predictions")
        st.info("Predictions will be displayed here")
    
    with col2:
        st.subheader("Volatility")
        st.info("Volatility analysis will be displayed here")
    
    st.subheader("Metrics")
    st.info("Key metrics will be displayed here")
