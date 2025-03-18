from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class ContinentModel(BaseModel):
    __tablename__ = "continent"

    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    population = Column(BigInteger, nullable=False)

    countries = relationship("CountryModel", back_populates="continent")
