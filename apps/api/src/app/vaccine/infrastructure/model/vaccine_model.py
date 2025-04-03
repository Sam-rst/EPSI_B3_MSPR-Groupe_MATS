from sqlalchemy import Column, BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from enum import Enum

from src.app.base.infrastructure.model.base_model import BaseModel
from src.app.daily_wise.infrastructure.model.daily_wise_vaccine_association import DailyWiseVaccineAssociation


class VaccineModel(BaseModel):
    __tablename__ = "vaccine"

    name = Column(String, nullable=False)
    laboratory = Column(String, nullable=False)
    technology = Column(String, nullable=True)
    dose = Column(String, nullable=True)
    efficacy = Column(Float, nullable=True)
    storage_temperature = Column(String, nullable=True)

    epidemic_id = Column(BigInteger, ForeignKey("epidemic.id"), nullable=False)
    epidemic = relationship("EpidemicModel", back_populates="vaccines")

    daylies = relationship("DailyWiseModel", secondary=DailyWiseVaccineAssociation, back_populates="vaccines")