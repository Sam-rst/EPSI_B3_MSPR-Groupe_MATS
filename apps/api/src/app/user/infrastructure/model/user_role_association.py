from sqlalchemy import Column, ForeignKey, BigInteger

from src.app.base.infrastructure.model.base_model import BaseModel


class UserRoleAssociation(BaseModel):
    __tablename__ = "user_role"

    user_id = Column(BigInteger, ForeignKey("user.id"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("role.id"), primary_key=True)
