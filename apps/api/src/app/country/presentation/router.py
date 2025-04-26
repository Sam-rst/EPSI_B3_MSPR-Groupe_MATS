from fastapi import APIRouter, status, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from src.core.middlewares.limiter import limiter

# =====Containers=====
from src.app.country.container import CountryContainer

# =====Usecases=====
from src.app.country.application.usecase.add_country_usecase import AddCountryUseCase
from src.app.country.application.usecase.find_all_countries_usecase import (
    FindAllCountriesUseCase,
)
from src.app.country.application.usecase.find_country_by_id_usecase import (
    FindCountryByIdUseCase,
)
from src.app.country.application.usecase.update_country_usecase import (
    UpdateCountryUseCase,
)
from src.app.country.application.usecase.delete_country_usecase import (
    DeleteCountryUseCase,
)
from src.app.country.application.usecase.import_countries_usecase import (
    ImportCountriesUseCase,
)

# =====Payloads=====
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.presentation.model.payload.update_country_payload import (
    UpdateCountryPayload,
)

# =====DTOs=====
from src.app.country.presentation.model.dto.bulk_insert_countries_response_dto import (
    BulkInsertCountriesResponseDTO,
)

country_router = APIRouter(
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


@country_router.get("")
@limiter.limit("2/minute")
@inject
def endpoint_usecase_get_all_countries(
    request: Request,
    usecase: FindAllCountriesUseCase = Depends(
        Provide[CountryContainer.find_all_countries_usecase]
    ),
):
    """
    Récupère tous les pays disponibles.

    Returns:
        JSONResponse: Une réponse contenant la liste des pays et leur nombre.
    """
    try:
        countries = usecase.execute()
        content = {"count": len(countries), "items": jsonable_encoder(countries)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@country_router.post("")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_add_country(
    request: Request,
    payload: CreateCountryPayload,
    usecase: AddCountryUseCase = Depends(Provide[CountryContainer.add_country_usecase]),
):
    """
    Crée un nouveau pays.

    Args:
        <body> payload (CreateCountryPayload): Les données nécessaires pour créer un pays.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation et l'ID du pays créé.
    """
    try:
        country = usecase.execute(payload)
        content = {
            "message": f"Le pays '{country.name}' a bien été créé portant l'id : {country.id}."
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


@country_router.get("/{id}")
@limiter.limit("20/minute")
@inject
def endpoint_usecase_get_country_by_id(
    request: Request,
    id: int,
    usecase: FindCountryByIdUseCase = Depends(
        Provide[CountryContainer.find_country_by_id_usecase]
    ),
):
    """
    Récupère les détails d'un pays spécifique.

    Args:
        <header> id (int): L'ID du pays à récupérer.

    Returns:
        JSONResponse: Une réponse contenant les détails du pays.
    """
    try:
        country = usecase.execute(id)
        content = {"item": jsonable_encoder(country)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@country_router.patch("/{id}")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_patch_country_by_id(
    request: Request,
    id: int,
    payload: UpdateCountryPayload,
    usecase: UpdateCountryUseCase = Depends(
        Provide[CountryContainer.update_country_usecase]
    ),
):
    """
    Met à jour les informations d'un pays existant.

    Args:
        <header> id (int): L'ID du pays à mettre à jour.
        <body> payload (UpdateCountryPayload): Les nouvelles données pour le pays.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        country = usecase.execute(id, payload)
        content = {"message": f"Le pays '{country.name}' a bien été modifié."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@country_router.delete("/{id}")
@limiter.limit("5/minute")
@inject
def endpoint_usecase_delete_country_by_id(
    request: Request,
    id: int,
    usecase: DeleteCountryUseCase = Depends(
        Provide[CountryContainer.delete_country_usecase]
    ),
):
    """
    Supprime un pays existant.

    Args:
        <header> id (int): L'ID du pays à supprimer.

    Returns:
        JSONResponse: Une réponse contenant un message de confirmation.
    """
    try:
        country = usecase.execute(id)
        content = {"message": f"Le pays '{country.name}' a bien été supprimé."}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@country_router.post(
    "/import",
    summary="Importer plusieurs pays",
)
@limiter.limit("1/hour")
@inject
def endpoint_usecase_import_continents(
    request: Request,
    payload: list[CreateCountryPayload],
    usecase: ImportCountriesUseCase = Depends(
        Provide[CountryContainer.import_countries_usecase]
    ),
):
    """
    Importe plusieurs pays à la fois.

    Args:
        <body> payload (list[CreateCountryPayload]): La liste des pays à importer.

    Returns:
        JSONResponse: Une réponse contenant le résultat de l'importation.
    """
    try:
        result: BulkInsertCountriesResponseDTO = usecase.execute(payload)
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
