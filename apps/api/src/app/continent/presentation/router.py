from fastapi import APIRouter, status, Request
from dependency_injector.wiring import inject
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.app.continent.container import ContinentContainer
from src.app.continent.presentation.model.payload.create_continent_pauload import (
    CreateContinentPayload,
)

continent_router = APIRouter(
    prefix="/continents",
    tags=["continents"],
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


@continent_router.get("")
@inject
def endpoint_usecase_get_all_continents():
    try:
        continent_repository = (
            ContinentContainer.get_repositories_container().get_repository_in_memory()
        )
        find_all_continents_usecase = (
            ContinentContainer.get_usecases_container().get_find_all_continents_usecase(
                continent_repository
            )
        )

        continents = find_all_continents_usecase.execute()
        content = {"items": jsonable_encoder(continents)}
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    except Exception as e:
        raise e


@continent_router.post("")
@inject
def endpoint_usecase_add_continent(
    payload: CreateContinentPayload,
    request: Request,
) -> JSONResponse:
    try:
        continent_repository = (
            ContinentContainer.get_repositories_container().get_repository_in_memory()
        )
        add_continent_usecase = (
            ContinentContainer.get_usecases_container().get_add_continent_usecase(
                continent_repository
            )
        )

        continent = add_continent_usecase.execute(payload)
        content = {"message": continent.print()}
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    except Exception as e:
        raise e


@continent_router.get("/{id}")
@inject
def endpoint_usecase_get_continent_by_id():
    pass


@continent_router.patch("/{id}")
@inject
def endpoint_usecase_patch_continent_by_id():
    pass


@continent_router.put("/{id}")
@inject
def endpoint_usecase_update_continent_by_id():
    pass


@inject
@continent_router.delete("/{id}")
def endpoint_usecase_delete_continent_by_id():
    pass
