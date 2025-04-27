from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from dependency_injector import providers
import jwt
from src.core.config.settings import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES


class JWTService:
    def __init__(self):
        try:
            if not JWT_SECRET_KEY:
                raise ValueError("JWT_SECRET_KEY must be set")
            self.secret_key = JWT_SECRET_KEY
            self.algorithm = "HS256"
            if not JWT_ACCESS_TOKEN_EXPIRES:
                raise ValueError("JWT_ACCESS_TOKEN_EXPIRES must be set")
            self.access_token_expire_seconds = (
                int(JWT_ACCESS_TOKEN_EXPIRES) if JWT_ACCESS_TOKEN_EXPIRES else 3600
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error configuration JWT Service: {str(e)}",
            )

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(
                    seconds=self.access_token_expire_seconds
                )
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
            return encoded_jwt

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating access token: {str(e)}",
            )

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.PyJWTError:
            raise ValueError("Invalid token")

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error verifying token: {str(e)}",
            )

jwt_service = JWTService()