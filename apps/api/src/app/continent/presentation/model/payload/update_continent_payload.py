from pydantic import BaseModel
from typing import Optional

class UpdateContinentPayload(BaseModel):
    name: Optional[str]
    code: Optional[str]
    population: Optional[int]