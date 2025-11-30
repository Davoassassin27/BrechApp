import polars as pl
import os

class DataCleaner:
    """
    Class to clean and normalize data using Polars.
    """
    def __init__(self):
        pass

    def process_json_to_parquet(self, input_path: str, output_path: str):
        """
        Reads a JSON file, cleans it, and saves it as Parquet.
        """
        try:
            # Read JSON
            df = pl.read_json(input_path)
            
            # Basic cleaning
            # Ensure 'fecha' is Date type
            if "fecha" in df.columns:
                df = df.with_columns(
                    pl.col("fecha").str.strptime(pl.Date, "%Y-%m-%d", strict=False)
                )
            
            # Ensure numeric columns
            for col in ["compra", "venta"]:
                if col in df.columns:
                    df = df.with_columns(pl.col(col).cast(pl.Float64))
            
            # Save to Parquet
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.write_parquet(output_path)
            print(f"Successfully converted {input_path} to {output_path}")
            return df
            
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return None
