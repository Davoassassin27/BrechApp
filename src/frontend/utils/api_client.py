import requests
from typing import Dict, Any, Optional
import pandas as pd


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_predictions(
        self,
        symbol: str,
        model: str = "arima",
        horizon: int = 30
    ) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/predictions/{symbol}"
        params = {"model": model, "horizon": horizon}
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def create_prediction(
        self,
        symbol: str,
        model: str = "arima",
        horizon: int = 30
    ) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/predictions"
        payload = {
            "symbol": symbol,
            "model": model,
            "horizon": horizon
        }
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_volatility(
        self,
        symbol: str,
        model: str = "rolling",
        window: int = 30
    ) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/volatility/{symbol}"
        params = {"model": model, "window": window}
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_historical_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d"
    ) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/historical/{symbol}"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_historical_stats(self, symbol: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/historical/{symbol}/stats"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/health")
            return response.status_code == 200
        except:
            return False
