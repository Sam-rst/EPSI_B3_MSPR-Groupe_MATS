from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class UpdateUserPayload(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    roles: Optional[list[str]] = None