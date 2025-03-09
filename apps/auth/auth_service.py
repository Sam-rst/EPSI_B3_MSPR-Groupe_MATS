from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import jwt
import datetime

SECRET_KEY = "mysecretkey"

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/token")
def generate_token(user: UserLogin):
    if user.username != "admin" or user.password != "password":
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {
        "sub": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/validate")
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}
