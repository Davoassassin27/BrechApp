import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPIEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "BrechApp API"
    
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_get_predictions(self):
        response = client.get("/api/v1/predictions/BTC-USD")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "BTC-USD"
    
    def test_create_prediction(self):
        payload = {
            "symbol": "BTC-USD",
            "model": "arima",
            "horizon": 30
        }
        response = client.post("/api/v1/predictions", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "BTC-USD"
        assert data["model"] == "arima"
    
    def test_get_volatility(self):
        response = client.get("/api/v1/volatility/BTC-USD")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "BTC-USD"
    
    def test_get_historical_data(self):
        response = client.get("/api/v1/historical/BTC-USD")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "BTC-USD"
    
    def test_get_historical_stats(self):
        response = client.get("/api/v1/historical/BTC-USD/stats")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert "mean" in data
        assert "std" in data


class TestAPIValidation:
    def test_invalid_interval(self):
        response = client.get("/api/v1/historical/BTC-USD?interval=invalid")
        assert response.status_code == 422
    
    def test_prediction_with_params(self):
        response = client.get("/api/v1/predictions/ETH-USD?model=prophet&horizon=60")
        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "prophet"
        assert data["horizon"] == 60
