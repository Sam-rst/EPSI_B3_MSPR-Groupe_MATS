from pydantic import BaseModel

class FindContinentByIdPayload(BaseModel):
    id: int