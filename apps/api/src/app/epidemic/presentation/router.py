from fastapi import APIRouter, status, HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# =====Containers=====
from src.app.epidemic.container import EpidemicContainer

# =====Usecases=====
from src.app.epidemic.application.usecase.add_epidemic_usecase import AddEpidemicUseCase
from src.app.epidemic.application.usecase.find_all_epidemics_usecase import (
    FindAllEpidemicsUseCase,
)
from src.app.epidemic.application.usecase.find_epidemic_by_id_usecase import (
    FindEpidemicByIdUseCase,
)
from src.app.epidemic.application.usecase.update_epidemic_usecase import (
    UpdateEpidemicUseCase,
)
from src.app.epidemic.application.usecase.delete_epidemic_usecase import (
    DeleteEpidemicUseCase,
)
from src.app.epidemic.application.usecase.import_epidemics_usecase import (
    ImportEpidemicsUseCase,
)

# =====Payloads=====
from src.app.epidemic.presentation.model.payload.create_epidemic_payload import (
    CreateEpidemicPayload,
)
from src.app.epidemic.presentation.model.payload.update_epidemic_payload import (
    UpdateEpidemicPayload,
)

# =====DTOs=====
from src.app.epidemic.presentation.model.dto.bulk_insert_epidemics_response_dto import (
    BulkInsertEpidemicsResponseDTO,
)

epidemic_router = APIRouter(
    tags=["epidemics"],
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


@epidemic_router.get("")
@inject
def endpoint_usecase_get_all_epidemics(
    usecase: FindAllEpidemicsUseCase = Depends(
        Provide[EpidemicContainer.find_all_epidemics_usecase]
    ),
):
    """
    Récupère toutes les épidémies disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des épidémies et leur nombre.
    """
    try:
        epidemics = usecase.execute()
        content = {"count": len(epidemics), "items": jsonable_encoder(epidemics)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@epidemic_router.post("")
@inject
def endpoint_usecase_add_epidemic(
    payload: CreateEpidemicPayload,
    usecase: AddEpidemicUseCase = Depends(
        Provide[EpidemicContainer.add_epidemic_usecase]
    ),
):
    """
    Crée une nouvelle épidémie.

    Args:
        <body> payload (CreateEpidemicPayload): Les données nécessaires pour créer une épidémie.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID de l'épidémie créée.
    """
    try:
        epidemic = usecase.execute(payload)
        content = {
            "message": f"L'épidémie '{epidemic.name}' a bien été créée portant l'id : {epidemic.id}."
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


@epidemic_router.get("/{id}")
@inject
def endpoint_usecase_get_epidemic_by_id(
    id: int,
    usecase: FindEpidemicByIdUseCase = Depends(
        Provide[EpidemicContainer.find_epidemic_by_id_usecase]
    ),
):
    """
    Récupère les détails d'une épidémie spécifique.

    Args:
        <header> id (int): L'ID de l'épidémie à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails de l'épidémie.
    """
    try:
        epidemic = usecase.execute(id)
        content = {"item": jsonable_encoder(epidemic)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@epidemic_router.patch("/{id}")
@inject
def endpoint_usecase_patch_epidemic_by_id(
    id: int,
    payload: UpdateEpidemicPayload,
    usecase: UpdateEpidemicUseCase = Depends(
        Provide[EpidemicContainer.update_epidemic_usecase]
    ),
):
    """
    Met à jour les informations d'une épidémie existante.

    Args:
        <header> id (int): L'ID de l'épidémie à mettre à jour.
        <body> payload (UpdateEpidemicPayload): Les nouvelles données pour l'épidémie.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        epidemic = usecase.execute(id, payload)
        content = {"message": f"L'épidémie '{epidemic.name}' a bien été modifiée."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@epidemic_router.delete("/{id}")
@inject
def endpoint_usecase_delete_epidemic_by_id(
    id: int,
    usecase: DeleteEpidemicUseCase = Depends(
        Provide[EpidemicContainer.delete_epidemic_usecase]
    ),
):
    """
    Supprime une épidémie existante.

    Args:
        <header> id (int): L'ID de l'épidémie à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        epidemic = usecase.execute(id)
        content = {"message": f"L'épidémie '{epidemic.name}' a bien été supprimée."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )

@epidemic_router.post(
    "/import",
    summary="Importer plusieurs epidemics",
)
@inject
def endpoint_usecase_import_continents(
    payload: list[CreateEpidemicPayload],
    usecase: ImportEpidemicsUseCase = Depends(
        Provide[EpidemicContainer.import_epidemics_usecase]
    ),
):
    """
    Importe plusieurs epidemics à la fois.

    Args:
        <body> payload (list[CreateEpidemicPayload]): La liste des continents à importer.

    Returns:
        JSONResponse: Une réponse contenant le résultat de l'importation.
    """
    try:
        result: BulkInsertEpidemicsResponseDTO = usecase.execute(payload)
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
