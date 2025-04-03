from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class CountryModel(BaseModel):
    __tablename__ = "country"

    name = Column(String, nullable=False)
    iso2 = Column(String, nullable=True)
    iso3 = Column(String, nullable=True)
    population = Column(BigInteger, nullable=True)

    continent_id = Column(BigInteger, ForeignKey("continent.id"))
    continent = relationship("ContinentModel", back_populates="countries")

    daylies = relationship("DailyWiseModel", back_populates="country")
