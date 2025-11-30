import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ingestion.api_client import APIClient

def save_raw_data():
    """
    Fetches data from API and saves it to data/raw.
    """
    client = APIClient()
    data = client.fetch_all_dollars()
    
    if not data:
        print("No data fetched.")
        return

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dolares_{timestamp}.json"
    
    # Ensure directory exists (it should, but good practice)
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    filepath = os.path.join(raw_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Data successfully saved to {filepath}")

if __name__ == "__main__":
    save_raw_data()
