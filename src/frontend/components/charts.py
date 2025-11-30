import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def plot_predictions(data: pd.DataFrame, title: str = "Price Predictions"):
    fig = go.Figure()
    
    if 'actual' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['actual'],
            mode='lines',
            name='Actual',
            line=dict(color='blue')
        ))
    
    if 'predicted' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['predicted'],
            mode='lines',
            name='Predicted',
            line=dict(color='red', dash='dash')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode='x unified'
    )
    
    return fig


def plot_volatility(data: pd.DataFrame, title: str = "Volatility Analysis"):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['volatility'],
        mode='lines',
        name='Volatility',
        fill='tozeroy',
        line=dict(color='orange')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Volatility",
        hovermode='x unified'
    )
    
    return fig


def plot_candlestick(data: pd.DataFrame, title: str = "Price Chart"):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    
    return fig
