from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from enum import Enum

from src.app.base.infrastructure.model.base_model import BaseModel


class EpidemicType(Enum):
    VIRUS = "virus"
    BACTERIA = "bacteria"
    PARASITE = "parasite"
    PRION = "prion"
    FUNGUS = "fungus"


class EpidemicModel(BaseModel):
    __tablename__ = "epidemic"

    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    pathogen_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    transmission_mode = Column(String, nullable=True)
    symptoms = Column(String, nullable=True)
    reproduction_rate = Column(Float, nullable=True)

    vaccines = relationship("VaccineModel", back_populates="epidemic")
    statistics = relationship("StatisticModel", back_populates="epidemic")
