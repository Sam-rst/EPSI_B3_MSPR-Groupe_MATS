from sqlalchemy import Column, BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from enum import Enum

from src.app.base.infrastructure.model.base_model import BaseModel
from src.app.user.infrastructure.model.user_role_association import UserRoleAssociation


class RoleModel(BaseModel):
    __tablename__ = "role"

    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    # Relation Many-to-Many avec UserModel
    users = relationship("UserModel", secondary=UserRoleAssociation.__table__, back_populates="roles")
