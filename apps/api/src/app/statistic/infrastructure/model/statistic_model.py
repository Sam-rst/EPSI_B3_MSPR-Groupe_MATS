from sqlalchemy import Column, BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class StatisticModel(BaseModel):
    __tablename__ = "statistic"

    label = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    published_at = Column(String, nullable=True)
    published_by = Column(String, nullable=True)

    country_id = Column(BigInteger, ForeignKey("country.id"), nullable=True)
    countries = relationship("CountryModel", back_populates="statistics")

    epidemic_id = Column(BigInteger, ForeignKey("epidemic.id"), nullable=True)
    epidemics = relationship("EpidemicModel", back_populates="statistics")

    daily_wise_id = Column(BigInteger, ForeignKey("daily_wise.id"), nullable=True)
    daily_wises = relationship("DailyWiseModel", back_populates="statistics")

    vaccine_id = Column(BigInteger, ForeignKey("vaccine.id"), nullable=True)
    vaccines = relationship("VaccineModel", back_populates="statistics")
