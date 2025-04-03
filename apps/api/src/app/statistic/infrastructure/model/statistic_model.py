from sqlalchemy import Column, BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel


class StatisticModel(BaseModel):
    __tablename__ = "statistic"

    label = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    published_at = Column(String, nullable=True)
    published_by = Column(String, nullable=True)

    country_id = Column(BigInteger, ForeignKey("country.id"), nullable=False)
    country = relationship("CountryModel", back_populates="statistics")

    epidemic_id = Column(BigInteger, ForeignKey("epidemic.id"), nullable=False)
    epidemic = relationship("EpidemicModel", back_populates="statistics")

    dayly_wise_id = Column(BigInteger, ForeignKey("daily_wise.id"), nullable=False)
    dayly_wise = relationship("DailyWiseModel", back_populates="statistics")
