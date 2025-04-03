from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, event, text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, nullable=True, server_default="system")
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.now,
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
    updated_by = Column(String, nullable=True, server_default="system")
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String, nullable=True)
    is_deleted = Column(Boolean, server_default=text("FALSE"))
