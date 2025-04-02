from typing import Optional
from pydantic import BaseModel

class UpdateCountryPayload(BaseModel):
    name: Optional[str]
    iso2: Optional[str]
    iso3: Optional[str]
    code3: Optional[str]
    population: Optional[int]