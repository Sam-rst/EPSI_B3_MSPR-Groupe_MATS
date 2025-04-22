from sqlalchemy import Column, String, BigInteger, ForeignKey
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

    country_id = Column(BigInteger, ForeignKey("country.id"))
    countries = relationship("CountryModel", back_populates="users")

    roles = relationship(
        "RoleModel",
        secondary=UserRoleAssociation.__tablename__,
        back_populates="users",
    )
