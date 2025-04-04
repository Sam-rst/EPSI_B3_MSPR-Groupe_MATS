from typing import Optional
from pydantic import BaseModel
from datetime import date


class UpdateEpidemicPayload(BaseModel):
    name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    type: Optional[str]
    pathogen_name: Optional[str]
    description: Optional[str]
    transmission_mode: Optional[str]
    symptoms: Optional[str]
    reproduction_rate: Optional[float]
