from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class CreateUserPayload(BaseModel):
  username: str
  password: str
  role_id: int
  region_id: int