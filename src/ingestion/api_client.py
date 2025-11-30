import requests
import pandas as pd
from typing import List, Dict, Any

class APIClient:
    """
    Client to fetch data from external APIs.
    """
    def __init__(self, base_url: str = "https://dolarapi.com/v1"):
        self.base_url = base_url

    def fetch_all_dollars(self) -> List[Dict[str, Any]]:
        """
        Fetch all dollar quotes from the API (DolarApi.com).
        Returns a list of dictionaries.
        """
        try:
            response = requests.get(f"{self.base_url}/dolares")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_history(self, casa: str) -> List[Dict[str, Any]]:
        """
        Fetch historical data for a specific 'casa' from ArgentinaDatos API.
        """
        url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{casa}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching history for {casa}: {e}")
            return []

    def get_as_dataframe(self) -> pd.DataFrame:
        """
        Fetch data and return as a Pandas DataFrame.
        """
        data = self.fetch_all_dollars()
        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()
