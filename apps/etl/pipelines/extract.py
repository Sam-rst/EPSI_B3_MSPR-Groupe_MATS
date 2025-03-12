import pandas as pd

def extract_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def extract_json(file_path: str) -> pd.DataFrame:
    return pd.read_json(file_path)
