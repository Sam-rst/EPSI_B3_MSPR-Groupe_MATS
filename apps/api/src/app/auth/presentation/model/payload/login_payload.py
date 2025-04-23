from pydantic import BaseModel


class LoginPayload(BaseModel):
    username: str
    password_hashed: str
