from typing import Optional
from pydantic import BaseModel

class UpdateVaccinePayload(BaseModel):
    name: Optional[str]