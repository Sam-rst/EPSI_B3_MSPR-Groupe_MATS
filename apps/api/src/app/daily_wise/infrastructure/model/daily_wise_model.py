from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class DailyWiseModel(BaseModel):
    __tablename__ = "daily_wise"

    date = Column(DateTime, nullable=False)
    province = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    country_id = Column(BigInteger, ForeignKey("country.id"), nullable=True)
    countries = relationship("CountryModel", back_populates="daily_wises")

    # Make sure this matches the property name in StatisticModel
    statistics = relationship("StatisticModel", back_populates="daily_wises")
