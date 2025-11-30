import pandas as pd

def calculate_gap(official_rate, parallel_rate):
    """
    Calculate the exchange rate gap percentage.
    """
    if official_rate == 0:
        return 0
    return ((parallel_rate - official_rate) / official_rate) * 100
