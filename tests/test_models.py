import pytest
import pandas as pd
import numpy as np
from src.models.time_series import ARIMAModel, ProphetModel
from src.models.volatility import GARCHModel, RollingVolatility
from src.models.predictor import Predictor


class TestARIMAModel:
    def test_arima_initialization(self):
        model = ARIMAModel(order=(1, 1, 1))
        assert model.order == (1, 1, 1)
        assert model.model is None
        assert model.fitted_model is None
    
    def test_arima_fit_predict(self):
        data = pd.Series(np.random.randn(100).cumsum())
        model = ARIMAModel(order=(1, 1, 1))
        model.fit(data)
        
        assert model.fitted_model is not None
        predictions = model.predict(steps=10)
        assert len(predictions) == 10


class TestProphetModel:
    def test_prophet_initialization(self):
        model = ProphetModel()
        assert model.fitted is False
    
    def test_prophet_fit_predict(self):
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        data = pd.Series(np.random.randn(100).cumsum(), index=dates)
        
        model = ProphetModel()
        model.fit(data)
        
        assert model.fitted is True
        forecast = model.predict(periods=10)
        assert len(forecast) == 110


class TestGARCHModel:
    def test_garch_initialization(self):
        model = GARCHModel(p=1, q=1)
        assert model.p == 1
        assert model.q == 1
        assert model.model is None
    
    def test_garch_fit_forecast(self):
        returns = pd.Series(np.random.randn(100) * 0.01)
        model = GARCHModel(p=1, q=1)
        model.fit(returns)
        
        assert model.fitted_model is not None
        forecast = model.forecast(horizon=5)
        assert len(forecast) == 5


class TestRollingVolatility:
    def test_rolling_volatility_initialization(self):
        vol = RollingVolatility(window=30)
        assert vol.window == 30
    
    def test_rolling_volatility_calculate(self):
        returns = pd.Series(np.random.randn(100) * 0.01)
        vol = RollingVolatility(window=30)
        
        rolling_vol = vol.calculate(returns)
        assert len(rolling_vol) == len(returns)
        assert rolling_vol.iloc[:29].isna().all()
    
    def test_rolling_volatility_annualized(self):
        returns = pd.Series(np.random.randn(100) * 0.01)
        vol = RollingVolatility(window=30)
        
        ann_vol = vol.calculate_annualized(returns, periods_per_year=252)
        assert len(ann_vol) == len(returns)


class TestPredictor:
    def test_predictor_initialization(self):
        predictor = Predictor()
        assert len(predictor.models) == 0
        assert len(predictor.fitted_models) == 0
    
    def test_predictor_add_model(self):
        predictor = Predictor()
        model = ARIMAModel()
        predictor.add_model('arima', model)
        
        assert 'arima' in predictor.models
        assert len(predictor.list_models()) == 1
    
    def test_predictor_fit_predict(self):
        data = pd.Series(np.random.randn(100).cumsum())
        predictor = Predictor()
        
        predictor.add_model('arima', ARIMAModel(order=(1, 1, 1)))
        predictor.fit(data, model_name='arima')
        
        assert 'arima' in predictor.fitted_models
        predictions = predictor.predict('arima', steps=10)
        assert len(predictions) == 10


class TestIntegration:
    def test_full_workflow(self):
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        prices = pd.Series(100 + np.random.randn(100).cumsum(), index=dates)
        returns = prices.pct_change().dropna()
        
        predictor = Predictor()
        predictor.add_model('arima', ARIMAModel(order=(1, 1, 1)))
        predictor.fit(prices, model_name='arima')
        
        predictions = predictor.predict('arima', steps=10)
        assert len(predictions) == 10
        
        vol_model = RollingVolatility(window=20)
        volatility = vol_model.calculate(returns)
        assert len(volatility) == len(returns)
