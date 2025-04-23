from fastapi import APIRouter, status, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# =====Containers=====
from src.app.auth.container import AuthContainer

# =====Usecases=====
from src.app.auth.application.usecase.register_user_usecase import RegisterUserUseCase
from src.app.auth.application.usecase.login_user_usecase import LoginUserUseCase
from src.app.auth.application.usecase.change_password_usecase import (
    ChangePasswordUseCase,
)
from src.app.auth.application.usecase.verify_token_usecase import VerifyTokenUseCase

# =====Payloads=====
from src.app.auth.presentation.model.payload.register_payload import RegisterPayload
from src.app.auth.presentation.model.payload.login_payload import LoginPayload

# =====Responses=====
from src.app.auth.presentation.model.response.register_response import RegisterResponse
from src.app.auth.presentation.model.response.login_response import LoginResponse

# =====Services=====
from src.app.auth.infrastructure.service.jwt_service import JWTService

auth_router = APIRouter(
    responses={
        status.HTTP_200_OK: {"description": "Ok"},
        status.HTTP_201_CREATED: {"description": "Created"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Unprocessable entity"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse
)
@inject
def register_user(
    payload: RegisterPayload,
    usecase: RegisterUserUseCase = Depends(
        Provide[AuthContainer.register_user_usecase]
    ),
):
    try:
        result = usecase.execute(payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result))
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponse
)
@inject
def login_user(
    payload: LoginPayload,
    usecase: LoginUserUseCase = Depends(Provide[AuthContainer.login_user_usecase]),
):
    try:
        result = usecase.execute(payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result))
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )

@auth_router.post("/forgot-password")
def forgot_password(email: str):
    # TODO : Implémenter l'envoi d'un mail de reset avec token
    raise HTTPException(status_code=501, detail="Not implemented yet")


@auth_router.post("/reset-password")
def reset_password(token: str, new_password: str):
    # TODO : Vérifier le token reçu et changer le mot de passe
    raise HTTPException(status_code=501, detail="Not implemented yet")


@auth_router.post("/verify-token")
@inject
def verify_token(
    token: str,
    usecase: VerifyTokenUseCase = Depends(Provide[AuthContainer.verify_token_usecase]),
):
    try:
        payload = usecase.execute(token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Token is valid", "payload": jsonable_encoder(payload)},
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
