def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(inplace=True)  # Suppression des valeurs manquantes
    df["date"] = pd.to_datetime(df["date"])  # Conversion de colonnes
    return df
