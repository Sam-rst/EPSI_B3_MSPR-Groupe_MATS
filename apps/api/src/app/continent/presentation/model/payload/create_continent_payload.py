from pydantic import BaseModel

class CreateContinentPayload(BaseModel):
    name: str
    code: str
    population: int