from typing import Optional
from pydantic import BaseModel


class UpdateVaccinePayload(BaseModel):
    name: Optional[str]
    laboratory: Optional[str]
    technology: Optional[str]
    dose: Optional[str]
    efficacy: Optional[float]
    storage_temperature: Optional[str]
    epidemic_id: Optional[int]
