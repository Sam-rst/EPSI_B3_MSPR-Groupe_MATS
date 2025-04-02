from sqlalchemy import Column, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.app.base.infrastructure.model.base_model import BaseModel


# Table d'association Many-to-Many entre daily_wise et vaccine
class DailyWiseVaccineAssociation(BaseModel):
    __tablename__ = "daily_wise_vaccine"

    daily_wise_id = Column(BigInteger, ForeignKey("daily_wise.id"))
    vaccine_id = Column(BigInteger, ForeignKey("vaccine.id"))
