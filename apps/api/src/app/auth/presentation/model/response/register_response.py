from pydantic import BaseModel


class RegisterResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    role_id: int
    country_id: int
