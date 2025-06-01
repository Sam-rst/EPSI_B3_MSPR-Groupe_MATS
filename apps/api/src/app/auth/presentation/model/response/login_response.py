from typing import Optional

from pydantic import BaseModel


class LoginResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    role_id: Optional[int] = None
    country_id: Optional[int] = None
    access_token: str
