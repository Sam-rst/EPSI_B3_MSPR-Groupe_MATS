from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel
from src.app.user.infrastructure.model.user_role_association import (
    UserRoleAssociation,
)


class UserModel(BaseModel):
    __tablename__ = "user"

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    birthdate = Column(String(10), nullable=True)

    roles = relationship(
        "RoleModel",
        secondary=UserRoleAssociation.__tablename__,
        back_populates="users",
    )
