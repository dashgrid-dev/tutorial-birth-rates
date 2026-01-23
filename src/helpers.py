"""Helper functions to read CSV data."""
import pandas as pd

def read_csv(path, skip_rows=0):
    """Read semicolon-separated CSV, return DataFrame."""
    return pd.read_csv(path, sep=';', skiprows=skip_rows, header=None, encoding='utf-8-sig')
