import os
import sys
import polars as pl

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.processing.cleaner import DataCleaner

def process_history():
    """
    Processes all historical JSON files and combines them into a single Parquet dataset.
    """
    cleaner = DataCleaner()
    
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw", "history")
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")
    output_path = os.path.join(processed_dir, "history.parquet")
    
    if not os.path.exists(raw_dir):
        print("No historical data found.")
        return

    dfs = []
    for filename in os.listdir(raw_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(raw_dir, filename)
            print(f"Processing {filename}...")
            
            # We use the cleaner to read and clean, but we want the DF back to combine
            # The cleaner.process_json_to_parquet saves individual files, but here we want to combine.
            # So let's use the logic from cleaner but keep it in memory or modify cleaner.
            # For simplicity, let's just use pl.read_json and clean here or use the cleaner's method if it returned the df.
            # I updated cleaner to return the df.
            
            # Temporary output for individual files (optional, or just skip saving individual parquets)
            temp_parquet = filepath.replace(".json", ".parquet")
            df = cleaner.process_json_to_parquet(filepath, temp_parquet)
            
            if df is not None:
                # Add 'casa' column if missing (it might be in the data, but let's ensure)
                # The filename is history_{casa}.json
                casa_name = filename.replace("history_", "").replace(".json", "")
                if "casa" not in df.columns:
                    df = df.with_columns(pl.lit(casa_name).alias("casa"))
                
                dfs.append(df)

    if dfs:
        # Concatenate all
        full_df = pl.concat(dfs, how="diagonal")
        
        # Save combined
        full_df.write_parquet(output_path)
        print(f"Combined history saved to {output_path}")
        print(full_df.head())
    else:
        print("No data processed.")

if __name__ == "__main__":
    process_history()
