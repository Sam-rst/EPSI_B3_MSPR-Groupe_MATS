from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "role"

    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    users = relationship("UserModel", back_populates="roles")
