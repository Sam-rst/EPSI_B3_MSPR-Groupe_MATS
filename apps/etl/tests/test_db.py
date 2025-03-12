from sqlalchemy import create_engine
from config.settings import settings

def test_database_connection():
    engine = create_engine(settings.DATABASE_URL)
    conn = engine.connect()
    assert conn.closed is False
    conn.close()
