from fastapi import APIRouter, status, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.core.middlewares.limiter import limiter
from src.core.dependencies import get_current_user

# =====Containers=====
from src.app.user.container import UserContainer

# =====Usecases=====
from src.app.user.application.usecase.find_user_by_id_usecase import FindUserByIdUseCase
from src.app.user.application.usecase.find_user_by_username_usecase import (
    FindUserByUsernameUseCase,
)
from src.app.user.application.usecase.delete_user_usecase import DeleteUserUseCase
from src.app.user.application.usecase.find_all_users_usecase import FindAllUsersUseCase

# Champs sensibles a exclure des reponses API (C3/C4 - ne jamais exposer le hash)
SENSITIVE_FIELDS = {"password", "password_hash"}


user_router = APIRouter(
    dependencies=[Depends(get_current_user)],
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


@user_router.get("")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_get_all_users(
    request: Request,
    usecase: FindAllUsersUseCase = Depends(
        Provide[UserContainer.find_all_users_usecase]
    ),
):
    """
    Récupère les détails des utilisateurs spécifiques.

    Args:

    Returns:
        JSONResponse: Une réponse contenant les détails des utilisateurs.
    """
    try:
        users = usecase.execute()
        content = {
            "count": len(users),
            "items": jsonable_encoder(users, exclude=SENSITIVE_FIELDS),
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.get("/id/{id}")
@limiter.limit("20/minute")
@inject
def endpoint_usecase_get_user_by_id(
    request: Request,
    id: int,
    usecase: FindUserByIdUseCase = Depends(
        Provide[UserContainer.find_user_by_id_usecase]
    ),
):
    """
    Récupère les détails d'un utilisateur spécifique.

    Args:
        <header> id (int): L'ID de l'utilisateur à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails de l'utilisateur.
    """
    try:
        user = usecase.execute(id)
        content = {"item": jsonable_encoder(user, exclude=SENSITIVE_FIELDS)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.get("/username/{username}")
@limiter.limit("20/minute")
@inject
def endpoint_usecase_get_user_by_username(
    request: Request,
    username: str,
    usecase: FindUserByUsernameUseCase = Depends(
        Provide[UserContainer.find_user_by_username_usecase]
    ),
):
    """
    Récupère les détails d'un utilisateur spécifique.

    Args:
        <header> username (int): Le username de l'utilisateur à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails de l'utilisateur.
    """
    try:
        user = usecase.execute(username)
        content = {"item": jsonable_encoder(user, exclude=SENSITIVE_FIELDS)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.delete("/{id}")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_delete_user_by_id(
    request: Request,
    id: int,
    current_user: dict = Depends(get_current_user),
    usecase: DeleteUserUseCase = Depends(Provide[UserContainer.delete_user_usecase]),
):
    """
    Supprime un utilisateur existant.
    Seul l'utilisateur lui-meme ou un admin (role_id=1) peut supprimer un compte.

    Args:
        <header> id (int): L'ID de l'utilisateur à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        # Verification d'ownership : seul le proprietaire ou un admin peut supprimer (fix IDOR C3)
        if current_user.get("id") != id and current_user.get("role_id") != 1:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "Acces non autorise : vous ne pouvez supprimer que votre propre compte."},
            )

        user = usecase.execute(id)
        content = {
            "message": f"L'utilisateur '{user.firstname} {user.lastname}' a bien ete supprime."
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
