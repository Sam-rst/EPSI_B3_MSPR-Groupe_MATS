from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from src.app.base.infrastructure.model.base_model import BaseModel
from src.app.daily_wise.infrastructure.model.daily_wise_vaccine_association import (
    DailyWiseVaccineAssociation,
)


class DailyWiseModel(BaseModel):
    __tablename__ = "daily_wise"

    date = Column(DateTime, nullable=False)
    province = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    country_id = Column(BigInteger, ForeignKey("country.id"), nullable=False)
    country = relationship("CountryModel", back_populates="daylies")

    statistics = relationship("StatisticModel", back_populates="daily_wise")

    vaccines = relationship(
        "VaccineModel", secondary=DailyWiseVaccineAssociation, back_populates="daylies"
    )
