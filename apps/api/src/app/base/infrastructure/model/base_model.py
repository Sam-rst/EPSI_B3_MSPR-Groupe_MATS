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

    def update(self, update_by: str):
        self.updated_at = datetime.now()
        self.updated_by = update_by

    def delete(self, deleted_by: str):
        self.deleted_at = datetime.now()
        self.deleted_by = deleted_by
        self.is_deleted = True
        self.update(deleted_by)

    def reactivate(self, updated_by: str):
        self.deleted_at = None
        self.deleted_by = None
        self.is_deleted = False
        self.update(updated_by)
