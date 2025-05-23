from pydantic import BaseModel

class CreateCountryPayload(BaseModel):
    name: str
    iso2: str
    iso3: str
    population: int
    continent_id: int