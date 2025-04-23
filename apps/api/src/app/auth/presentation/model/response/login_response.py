from pydantic import BaseModel


class LoginResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    # role: str
    role_id: int
    # country: str
    country_id: int
    access_token: str
