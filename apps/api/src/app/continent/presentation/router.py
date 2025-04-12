from fastapi import APIRouter, HTTPException, status
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# =====Containers=====
from src.app.continent.container import ContinentContainer

# =====Usecases=====
from src.app.continent.application.usecase.add_continent_usecase import (
    AddContinentUseCase,
)
from src.app.continent.application.usecase.find_all_continents_usecase import (
    FindAllContinentsUseCase,
)
from src.app.continent.application.usecase.find_continent_by_id_usecase import (
    FindContinentByIdUseCase,
)
from src.app.continent.application.usecase.update_continent_usecase import (
    UpdateContinentUseCase,
)
from src.app.continent.application.usecase.delete_continent_usecase import (
    DeleteContinentUseCase,
)
from src.app.continent.application.usecase.import_continents_usecase import (
    ImportContinentsUseCase,
)

# =====Payloads=====
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.presentation.model.payload.update_continent_payload import (
    UpdateContinentPayload,
)

# =====DTOs=====
from src.app.continent.presentation.model.dto.bulk_insert_continents_response_dto import (
    BulkInsertContinentsResponseDTO,
)

continent_router = APIRouter(
    tags=["Continents"],
    responses={
        status.HTTP_200_OK: {"description": "Requête réussie"},
        status.HTTP_201_CREATED: {"description": "Ressource créée avec succès"},
        status.HTTP_400_BAD_REQUEST: {"description": "Requête invalide"},
        status.HTTP_404_NOT_FOUND: {"description": "Ressource non trouvée"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erreur interne du serveur"
        },
    },
)


@continent_router.get(
    "",
    summary="Récupérer tous les continents",
)
@inject
def endpoint_usecase_get_all_continents(
    usecase: FindAllContinentsUseCase = Depends(
        Provide[ContinentContainer.find_all_continents_usecase]
    ),
):
    """
    Récupère tous les continents disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des continents et leur nombre.
    """
    try:
        continents = usecase.execute()
        content = {"count": len(continents), "items": jsonable_encoder(continents)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@continent_router.post(
    "",
    summary="Créer un nouveau continent",
)
@inject
def endpoint_usecase_add_continent(
    payload: CreateContinentPayload,
    usecase: AddContinentUseCase = Depends(
        Provide[ContinentContainer.add_continent_usecase]
    ),
):
    """
    Crée un nouveau continent.

    Args:
        <body> payload: CreateContinentPayload --> Les données nécessaires pour créer un continent.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID du continent créé.
    """
    try:
        continent = usecase.execute(payload)
        content = {
            "message": f"Le continent '{continent.name}' a bien été créé portant l'id : {continent.id}."
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


@continent_router.get(
    "/{id}",
    summary="Récupérer un continent par ID",
)
@inject
def endpoint_usecase_get_continent_by_id(
    id: int,
    usecase: FindContinentByIdUseCase = Depends(
        Provide[ContinentContainer.find_continent_by_id_usecase]
    ),
):
    """
    Récupère les détails d'un continent spécifique.

    Args:
        <header> id (int): L'ID du continent à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails du continent.
    """
    try:
        continent = usecase.execute(id)
        content = {"item": jsonable_encoder(continent)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@continent_router.patch(
    "/{id}",
    summary="Mettre à jour un continent",
)
@inject
def endpoint_usecase_patch_continent_by_id(
    id: int,
    payload: UpdateContinentPayload,
    usecase: UpdateContinentUseCase = Depends(
        Provide[ContinentContainer.update_continent_usecase]
    ),
):
    """
    Met à jour les informations d'un continent existant.

    Args:
        <header> id (int): L'ID du continent à mettre à jour.
        <body> payload (UpdateContinentPayload): Les nouvelles données pour le continent.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        continent = usecase.execute(id, payload)
        content = {"message": f"Le continent '{continent.name}' a bien été modifié."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@continent_router.delete(
    "/{id}",
    summary="Supprimer un continent",
)
@inject
def endpoint_usecase_delete_continent_by_id(
    id: int,
    usecase: DeleteContinentUseCase = Depends(
        Provide[ContinentContainer.delete_continent_usecase]
    ),
):
    """
    Supprime un continent existant.

    Args:
        <header> id (int): L'ID du continent à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        continent = usecase.execute(id)
        content = {"message": f"Le continent '{continent.name}' a bien été supprimé."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@continent_router.post(
    "/import",
    summary="Importer plusieurs continents",
)
@inject
def endpoint_usecase_import_continents(
    payload: list[CreateContinentPayload],
    usecase: ImportContinentsUseCase = Depends(
        Provide[ContinentContainer.import_continents_usecase]
    ),
):
    """
    Importe plusieurs continents à la fois.

    Args:
        <body> payload (list[CreateContinentPayload]): La liste des continents à importer.

    Returns:
        JSONResponse: Une réponse contenant le résultat de l'importation.
    """
    try:
        result: BulkInsertContinentsResponseDTO = usecase.execute(payload)
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
