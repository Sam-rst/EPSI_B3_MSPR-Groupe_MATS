from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    country_id = Column(BigInteger, ForeignKey("country.id"))
    countries = relationship("CountryModel", back_populates="users")

    role_id = Column(BigInteger, ForeignKey("role.id"))
    roles = relationship("RoleModel", back_populates="users")
