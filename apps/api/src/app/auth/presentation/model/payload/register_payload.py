from typing import Optional

from pydantic import BaseModel


class RegisterPayload(BaseModel):
    username: str
    password: str
    role_id: Optional[int] = None
    country_id: Optional[int] = None
