from pydantic import BaseModel

class CreateVaccinePayload(BaseModel):
    name: str
    laboratory: str
    technology: str | None = None
    dose: str | None = None
    efficacy: float | None = None
    storage_temperature: str | None = None
    epidemic_id: int