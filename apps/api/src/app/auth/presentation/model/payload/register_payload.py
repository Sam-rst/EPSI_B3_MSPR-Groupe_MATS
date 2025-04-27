from pydantic import BaseModel


class RegisterPayload(BaseModel):
    username: str
    password: str
    role_id: int
    country_id: int
