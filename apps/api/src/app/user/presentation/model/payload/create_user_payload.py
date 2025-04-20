from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class CreateUserPayload(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str
    gender: Optional[str] = None
    birthdate: Optional[date] = None