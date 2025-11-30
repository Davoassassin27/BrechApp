import pandas as pd
import numpy as np
from arch import arch_model


class GARCHModel:
    def __init__(self, p=1, q=1):
        self.p = p
        self.q = q
        self.model = None
        self.fitted_model = None
    
    def fit(self, returns):
        returns_pct = returns * 100
        self.model = arch_model(returns_pct, vol='Garch', p=self.p, q=self.q)
        self.fitted_model = self.model.fit(disp='off')
        return self
    
    def forecast(self, horizon=30):
        if self.fitted_model is None:
            raise ValueError("Model must be fitted before forecasting")
        forecast = self.fitted_model.forecast(horizon=horizon)
        return forecast.variance.values[-1, :]
    
    def get_conditional_volatility(self):
        if self.fitted_model is None:
            return None
        return self.fitted_model.conditional_volatility


class RollingVolatility:
    def __init__(self, window=30):
        self.window = window
    
    def calculate(self, returns):
        return returns.rolling(window=self.window).std()
    
    def calculate_annualized(self, returns, periods_per_year=252):
        rolling_vol = self.calculate(returns)
        return rolling_vol * np.sqrt(periods_per_year)
    
    def calculate_ewm(self, returns, span=30):
        return returns.ewm(span=span).std()
