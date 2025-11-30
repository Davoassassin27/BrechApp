import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet


class ARIMAModel:
    def __init__(self, order=(1, 1, 1)):
        self.order = order
        self.model = None
        self.fitted_model = None
    
    def fit(self, data):
        self.model = ARIMA(data, order=self.order)
        self.fitted_model = self.model.fit()
        return self
    
    def predict(self, steps=30):
        if self.fitted_model is None:
            raise ValueError("Model must be fitted before prediction")
        return self.fitted_model.forecast(steps=steps)
    
    def get_params(self):
        if self.fitted_model is None:
            return None
        return self.fitted_model.params


class ProphetModel:
    def __init__(self):
        self.model = Prophet()
        self.fitted = False
    
    def fit(self, data, date_col='ds', value_col='y'):
        df = pd.DataFrame({
            'ds': data.index if date_col == 'ds' else data[date_col],
            'y': data.values if value_col == 'y' else data[value_col]
        })
        self.model.fit(df)
        self.fitted = True
        return self
    
    def predict(self, periods=30, freq='D'):
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction")
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
