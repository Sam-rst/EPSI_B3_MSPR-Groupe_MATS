from sqlalchemy import Column, BigInteger, String
from src.app.base.infrastructure.model.base_model import BaseModel

class CountryModel(BaseModel):
    __tablename__ = "country"

    name = Column(String, nullable=False)
    iso2 = Column(String, nullable=False)
    iso3 = Column(String, nullable=False)
    code3 = Column(String, nullable=False)
    population = Column(BigInteger, nullable=False)