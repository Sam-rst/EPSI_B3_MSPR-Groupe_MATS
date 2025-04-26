from fastapi import APIRouter, status, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.core.middlewares.limiter import limiter

# =====Containers=====
from src.app.role.container import RoleContainer

# =====Usecases=====
from src.app.role.application.usecase.add_role_usecase import AddRoleUseCase
from src.app.role.application.usecase.find_all_roles_usecase import FindAllRolesUseCase
from src.app.role.application.usecase.find_role_by_id_usecase import FindRoleByIdUseCase
from src.app.role.application.usecase.update_role_usecase import UpdateRoleUseCase
from src.app.role.application.usecase.delete_role_usecase import DeleteRoleUseCase
from src.app.role.application.usecase.import_roles_usecase import ImportRolesUseCase

# =====Payloads=====
from src.app.role.presentation.model.payload.create_role_payload import CreateRolePayload
from src.app.role.presentation.model.payload.update_role_payload import UpdateRolePayload

# =====DTO=====
from src.app.role.presentation.model.dto.bulk_insert_roles_response_dto import (
    BulkInsertRolesResponseDTO,
)

role_router = APIRouter(
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


@role_router.get(
    "",
    summary="Récupérer tous les rôles",
)
@limiter.limit("2/minute")
@inject
def endpoint_usecase_get_all_roles(
    request: Request,
    usecase: FindAllRolesUseCase = Depends(
        Provide[RoleContainer.find_all_roles_usecase]
    ),
):
    """
    Récupère tous les roles disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des roles et leur nombre.
    """
    try:
        roles = usecase.execute()
        content = {"count": len(roles), "items": jsonable_encoder(roles)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@role_router.post(
    "",
    summary="Créer un nouveau role",
)
@limiter.limit("5/minute")
@inject
def endpoint_usecase_add_role(
    request: Request,
    payload: CreateRolePayload,
    usecase: AddRoleUseCase = Depends(
        Provide[RoleContainer.add_role_usecase]
    ),
):
    """
    Crée un nouveau role.

    Args:
        <body> payload: CreateRolePayload --> Les données nécessaires pour créer un role.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID du role créé.
    """
    try:
        role = usecase.execute(payload)
        content = {
            "message": f"Le rôle '{role.name}' a bien été créé portant l'id : {role.id}."
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


@role_router.get(
    "/{id}",
    summary="Récupérer un role par son ID",
)
@limiter.limit("20/minute")
@inject
def endpoint_usecase_get_role_by_id(
    request: Request,
    id: int,
    usecase: FindRoleByIdUseCase = Depends(
        Provide[RoleContainer.find_role_by_id_usecase]
    ),
):
    """
    Récupère les détails d'un role spécifique.

    Args:
        <header> id (int): L'ID du role à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails du role.
    """
    try:
        role = usecase.execute(id)
        content = {"item": jsonable_encoder(role)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@role_router.patch(
    "/{id}",
    summary="Mettre à jour un role",
)
@limiter.limit("5/minute")
@inject
def endpoint_usecase_patch_role_by_id(
    request: Request,
    id: int,
    payload: UpdateRolePayload,
    usecase: UpdateRoleUseCase = Depends(
        Provide[RoleContainer.update_role_usecase]
    ),
):
    """
    Met à jour les informations d'un role existant.

    Args:
        <header> id (int): L'ID du role à mettre à jour.
        <body> payload (UpdateRolePayload): Les nouvelles données pour le role.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        role = usecase.execute(id, payload)
        content = {"message": f"Le role '{role.name}' a bien été modifié."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@role_router.delete(
    "/{id}",
    summary="Supprimer un role",
)
@limiter.limit("5/minute")
@inject
def endpoint_usecase_delete_role_by_id(
    request: Request,
    id: int,
    usecase: DeleteRoleUseCase = Depends(
        Provide[RoleContainer.delete_role_usecase]
    ),
):
    """
    Supprime un role existant.

    Args:
        <header> id (int): L'ID du role à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        role = usecase.execute(id)
        content = {"message": f"Le role '{role.name}' a bien été supprimé."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@role_router.post(
    "/import",
    summary="Importer plusieurs roles",
)
@limiter.limit("1/hour")
@inject
def endpoint_usecase_import_roles(
    request: Request,
    payload: list[CreateRolePayload],
    usecase: ImportRolesUseCase = Depends(
        Provide[RoleContainer.import_roles_usecase]
    ),
):
    """
    Importe plusieurs roles à la fois.

    Args:
        <body> payload (list[CreateRolePayload]): La liste des roles à importer.

    Returns:
        JSONResponse: Une réponse contenant le résultat de l'importation.
    """
    try:
        result: BulkInsertRolesResponseDTO = usecase.execute(payload)
        content = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
