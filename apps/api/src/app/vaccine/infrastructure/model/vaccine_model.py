from sqlalchemy import Column, String, DateTime
from src.app.base.infrastructure.model.base_model import BaseModel

class VaccineModel(BaseModel):
    __tablename__ = "vaccine"

    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
    created_by = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)