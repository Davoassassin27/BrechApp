import streamlit as st
from typing import Dict, Any


def display_metrics(metrics: Dict[str, Any]):
    cols = st.columns(len(metrics))
    
    for col, (key, value) in zip(cols, metrics.items()):
        with col:
            st.metric(
                label=key.replace('_', ' ').title(),
                value=value
            )


def display_metric_card(label: str, value: Any, delta: Any = None):
    st.metric(label=label, value=value, delta=delta)


def display_statistics(data: Dict[str, float]):
    st.subheader("Statistical Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean", f"{data.get('mean', 0):.2f}")
    
    with col2:
        st.metric("Std Dev", f"{data.get('std', 0):.2f}")
    
    with col3:
        st.metric("Min", f"{data.get('min', 0):.2f}")
    
    with col4:
        st.metric("Max", f"{data.get('max', 0):.2f}")


def display_model_performance(metrics: Dict[str, float]):
    st.subheader("Model Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("MAE", f"{metrics.get('mae', 0):.4f}")
    
    with col2:
        st.metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
    
    with col3:
        st.metric("R²", f"{metrics.get('r2', 0):.4f}")
