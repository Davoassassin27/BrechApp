import os
import sys
import json
from datetime import datetime
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ingestion.api_client import APIClient

def ingest_history():
    """
    Fetches historical data for multiple dollar types and saves them.
    """
    client = APIClient()
    casas = ["oficial", "blue", "mep", "contadoconliqui", "mayorista"]
    
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw", "history")
    os.makedirs(raw_dir, exist_ok=True)
    
    for casa in casas:
        print(f"Fetching history for {casa}...")
        data = client.fetch_history(casa)
        
        if data:
            filename = f"history_{casa}.json"
            filepath = os.path.join(raw_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Saved {len(data)} records to {filepath}")
        else:
            print(f"No data found for {casa}")
        
        time.sleep(1) # Be nice to the API

if __name__ == "__main__":
    ingest_history()
