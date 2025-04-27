from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class UpdateUserPayload(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    region: Optional[date] = None