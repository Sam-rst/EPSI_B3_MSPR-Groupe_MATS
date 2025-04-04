from typing import Optional
from pydantic import BaseModel
from datetime import date


class CreateEpidemicPayload(BaseModel):
    name: str
    start_date: date
    end_date: date
    type: str
    pathogen_name: str
    description: Optional[str]
    transmission_mode: Optional[str]
    symptoms: Optional[str]
    reproduction_rate: Optional[float]
