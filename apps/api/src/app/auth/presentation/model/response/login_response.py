from pydantic import BaseModel


class LoginResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    role_id: int
    country_id: int
    access_token: str
