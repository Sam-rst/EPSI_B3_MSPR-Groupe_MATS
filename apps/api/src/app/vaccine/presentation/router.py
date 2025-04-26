from fastapi import APIRouter, status, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.core.middlewares.limiter import limiter

# =====Containers=====
from src.app.vaccine.container import VaccineContainer

# =====Usecases=====
from src.app.vaccine.application.usecase.add_vaccine_usecase import AddVaccineUseCase
from src.app.vaccine.application.usecase.find_all_vaccines_usecase import (
    FindAllVaccinesUseCase,
)
from src.app.vaccine.application.usecase.find_vaccine_by_id_usecase import (
    FindVaccineByIdUseCase,
)
from src.app.vaccine.application.usecase.update_vaccine_usecase import (
    UpdateVaccineUseCase,
)
from src.app.vaccine.application.usecase.delete_vaccine_usecase import (
    DeleteVaccineUseCase,
)
from src.app.vaccine.application.usecase.import_vaccines_usecase import (
    ImportVaccinesUseCase,
)

# =====Payloads=====
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)

# =====DTOs=====
from src.app.vaccine.presentation.model.dto.bulk_insert_vaccines_response_dto import (
    BulkInsertVaccinesResponseDTO,
)

vaccine_router = APIRouter(
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


@vaccine_router.get("")
@limiter.limit("2/minute")
@inject
def endpoint_usecase_get_all_vaccines(
    request: Request,
    usecase: FindAllVaccinesUseCase = Depends(
        Provide[VaccineContainer.find_all_vaccines_usecase]
    ),
):
    """
    Récupère tous les vaccins disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des vaccins et leur nombre.
    """
    try:
        vaccines = usecase.execute()
        content = {"count": len(vaccines), "items": jsonable_encoder(vaccines)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@vaccine_router.post("")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_add_vaccine(
    request: Request,
    payload: CreateVaccinePayload,
    usecase: AddVaccineUseCase = Depends(Provide[VaccineContainer.add_vaccine_usecase]),
):
    """
    Crée un nouveau vaccin.

    Args:
        <body> payload (CreateVaccinePayload): Les données nécessaires pour créer un vaccin.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID du vaccin créé.
    """
    try:
        vaccine = usecase.execute(payload)
        content = {
            "message": f"Le vaccin '{vaccine.name}' a bien été créé portant l'id : {vaccine.id}."
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


@vaccine_router.get("/{id}")
@limiter.limit("20/minute")
@inject
def endpoint_usecase_get_vaccine_by_id(
    request: Request,
    id: int,
    usecase: FindVaccineByIdUseCase = Depends(
        Provide[VaccineContainer.find_vaccine_by_id_usecase]
    ),
):
    """
    Récupère les détails d'un vaccin spécifique.

    Args:
        <header> id (int): L'ID du vaccin à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails du vaccin.
    """
    try:
        vaccine = usecase.execute(id)
        content = {"item": jsonable_encoder(vaccine)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@vaccine_router.patch("/{id}")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_patch_vaccine_by_id(
    request: Request,
    id: int,
    payload: UpdateVaccinePayload,
    usecase: UpdateVaccineUseCase = Depends(
        Provide[VaccineContainer.update_vaccine_usecase]
    ),
):
    """
    Met à jour les informations d'un vaccin existant.

    Args:
        <header> id (int): L'ID du vaccin à mettre à jour.
        <body> payload (UpdateVaccinePayload): Les nouvelles données pour le vaccin.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        vaccine = usecase.execute(id, payload)
        content = {"message": f"Le vaccin '{vaccine.name}' a bien été modifié."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@vaccine_router.delete("/{id}")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_delete_vaccine_by_id(
    request: Request,
    id: int,
    usecase: DeleteVaccineUseCase = Depends(
        Provide[VaccineContainer.delete_vaccine_usecase]
    ),
):
    """
    Supprime un vaccin existant.

    Args:
        <header> id (int): L'ID du vaccin à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        vaccine = usecase.execute(id)
        content = {"message": f"Le vaccin '{vaccine.name}' a bien été supprimé."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@vaccine_router.post(
    "/import",
    summary="Importer plusieurs vaccins",
)
@limiter.limit("1/hour")
@inject
def endpoint_usecase_import_continents(
    request: Request,
    payload: list[CreateVaccinePayload],
    usecase: ImportVaccinesUseCase = Depends(
        Provide[VaccineContainer.import_vaccines_usecase]
    ),
):
    """
    Importe plusieurs vaccines à la fois.

    Args:
        <body> payload (list[CreateVaccinePayload]): La liste des vaccines à importer.

    Returns:
        JSONResponse: Une réponse contenant le résultat de l'importation.
    """
    try:
        result: BulkInsertVaccinesResponseDTO = usecase.execute(payload)
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
