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

# =====Payloads=====
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.presentation.model.payload.update_continent_payload import (
    UpdateContinentPayload,
)
from src.app.continent.application.usecase.delete_continent_usecase import (
    DeleteContinentUseCase,
)

continent_router = APIRouter(
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
def endpoint_usecase_get_all_continents(
    usecase: FindAllContinentsUseCase = Depends(
        Provide[ContinentContainer.find_all_continents_usecase]
    ),
):
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


@continent_router.post("")
@inject
def endpoint_usecase_add_continent(
    payload: CreateContinentPayload,
    usecase: AddContinentUseCase = Depends(
        Provide[ContinentContainer.add_continent_usecase]
    ),
):
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


@continent_router.get("/{id}")
@inject
def endpoint_usecase_get_continent_by_id(
    id: int,
    usecase: FindContinentByIdUseCase = Depends(
        Provide[ContinentContainer.find_continent_by_id_usecase]
    ),
):
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


@continent_router.patch("/{id}")
@inject
def endpoint_usecase_patch_continent_by_id(
    id: int,
    payload: UpdateContinentPayload,
    usecase: UpdateContinentUseCase = Depends(
        Provide[ContinentContainer.update_continent_usecase]
    ),
):
    try:
        continent = usecase.execute(id, payload)
        content = {
            "message": f"Le continent '{continent.name}' a bien été modifié."
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


@continent_router.delete("/{id}")
@inject
def endpoint_usecase_delete_continent_by_id(
    id: int,
    usecase: DeleteContinentUseCase = Depends(
        Provide[ContinentContainer.delete_continent_usecase]
    ),
):
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
