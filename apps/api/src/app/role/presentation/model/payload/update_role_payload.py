from typing import Optional
from pydantic import BaseModel


class UpdateRolePayload(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
