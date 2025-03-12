from sqlalchemy import create_engine
import os
from config.settings import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

def load_data(df: pd.DataFrame, table_name: str):
    df.to_sql(table_name, engine, if_exists="append", index=False)
