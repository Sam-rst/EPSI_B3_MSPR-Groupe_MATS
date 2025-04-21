from fastapi import APIRouter, status, HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# =====Containers=====
from src.app.user.container import UserContainer

# =====Usecases=====
from src.app.user.application.usecase.add_user_usecase import AddUserUseCase
from src.app.user.application.usecase.find_all_users_usecase import FindAllUsersUseCase
from src.app.user.application.usecase.find_user_by_id_usecase import FindUserByIdUseCase
from src.app.user.application.usecase.update_user_usecase import UpdateUserUseCase
from src.app.user.application.usecase.delete_user_usecase import DeleteUserUseCase

# =====Payloads=====
from src.app.user.presentation.model.payload.create_user_payload import CreateUserPayload
from src.app.user.presentation.model.payload.update_user_payload import UpdateUserPayload

user_router = APIRouter(
    tags=["users"],
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
@inject
def endpoint_usecase_get_all_users(
    usecase: FindAllUsersUseCase = Depends(
        Provide[UserContainer.find_all_users_usecase]
    ),
):
    """
    Récupère tous les utilisateurs disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des utilisateurs et leur nombre.
    """
    try:
        users = usecase.execute()
        content = {"count": len(users), "items": jsonable_encoder(users)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.post("")
@inject
def endpoint_usecase_add_user(
    payload: CreateUserPayload,
    usecase: AddUserUseCase = Depends(Provide[UserContainer.add_user_usecase]),
):
    """
    Crée un nouvel utilisateur.

    Args:
        <body> payload (CreateUserPayload): Les données nécessaires pour créer un utilisateur.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID de l'utilisateur créé.
    """
    try:
        user = usecase.execute(payload)
        content = {
            "message": f"L'utilisateur '{user.firstname} {user.lastname}' a bien été créé avec l'id : {user.id}."
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.get("/{id}")
@inject
def endpoint_usecase_get_user_by_id(
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
        content = {"item": jsonable_encoder(user)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@user_router.patch("/{id}")
@inject
def endpoint_usecase_patch_user_by_id(
    id: int,
    payload: UpdateUserPayload,
    usecase: UpdateUserUseCase = Depends(
        Provide[UserContainer.update_user_usecase]
    ),
):
    """
    Met à jour les informations d'un utilisateur existant.

    Args:
        <header> id (int): L'ID de l'utilisateur à mettre à jour.
        <body> payload (UpdateUserPayload): Les nouvelles données pour l'utilisateur.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        user = usecase.execute(id, payload)
        content = {"message": f"L'utilisateur '{user.firstname} {user.lastname}' a bien été modifié."}
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
@inject
def endpoint_usecase_delete_user_by_id(
    id: int,
    usecase: DeleteUserUseCase = Depends(
        Provide[UserContainer.delete_user_usecase]
    ),
):
    """
    Supprime un utilisateur existant.

    Args:
        <header> id (int): L'ID de l'utilisateur à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        user = usecase.execute(id)
        content = {"message": f"L'utilisateur '{user.firstname} {user.lastname}' a bien été supprimé."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )