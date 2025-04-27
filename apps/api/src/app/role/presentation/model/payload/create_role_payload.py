from typing import Optional
from pydantic import BaseModel


class CreateRolePayload(BaseModel):
    name: str
    description: Optional[str] = None
