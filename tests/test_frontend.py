import pytest
from src.frontend.utils.api_client import APIClient


class TestAPIClient:
    def setup_method(self):
        self.client = APIClient(base_url="http://localhost:8000/api/v1")
    
    def test_client_initialization(self):
        assert self.client.base_url == "http://localhost:8000/api/v1"
        assert self.client.session is not None
    
    def test_get_predictions_structure(self):
        result = self.client.get_predictions("BTC-USD", model="arima", horizon=30)
        assert isinstance(result, dict)
    
    def test_create_prediction_structure(self):
        result = self.client.create_prediction("BTC-USD", model="arima", horizon=30)
        assert isinstance(result, dict)
    
    def test_get_volatility_structure(self):
        result = self.client.get_volatility("BTC-USD", model="rolling", window=30)
        assert isinstance(result, dict)
    
    def test_get_historical_data_structure(self):
        result = self.client.get_historical_data("BTC-USD", interval="1d")
        assert isinstance(result, dict)
    
    def test_get_historical_stats_structure(self):
        result = self.client.get_historical_stats("BTC-USD")
        assert isinstance(result, dict)
