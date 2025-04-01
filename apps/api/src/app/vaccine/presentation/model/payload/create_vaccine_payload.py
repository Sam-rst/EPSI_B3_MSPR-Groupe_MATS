from pydantic import BaseModel

class CreateVaccinePayload(BaseModel):
    name: str