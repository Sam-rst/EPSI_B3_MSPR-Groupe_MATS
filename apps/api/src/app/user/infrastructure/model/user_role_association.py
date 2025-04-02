from sqlalchemy import Column, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.app.base.infrastructure.model.base_model import BaseModel


# Table d'association Many-to-Many entre user et role
class UserRoleAssociation(BaseModel):
    __tablename__ = "user_role"

    user_id = Column(BigInteger, ForeignKey("user.id"))
    role_id = Column(BigInteger, ForeignKey("role.id"))
