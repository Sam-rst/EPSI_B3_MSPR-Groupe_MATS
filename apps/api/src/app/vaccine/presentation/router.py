from fastapi import APIRouter, status, HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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

# =====Payloads=====
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)

vaccine_router = APIRouter(
    tags=["vaccines"],
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
@inject
def endpoint_usecase_get_all_vaccines(
    usecase: FindAllVaccinesUseCase = Depends(
        Provide[VaccineContainer.find_all_vaccines_usecase]
    ),
):
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
@inject
def endpoint_usecase_add_vaccine(
    payload: CreateVaccinePayload,
    usecase: AddVaccineUseCase = Depends(
        Provide[VaccineContainer.add_vaccine_usecase]
    ),
):
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
@inject
def endpoint_usecase_get_vaccine_by_id(
    id: int,
    usecase: FindVaccineByIdUseCase = Depends(
        Provide[VaccineContainer.find_vaccine_by_id_usecase]
    ),
):
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
@inject
def endpoint_usecase_patch_vaccine_by_id(
    id: int,
    payload: UpdateVaccinePayload,
    usecase: UpdateVaccineUseCase = Depends(
        Provide[VaccineContainer.update_vaccine_usecase]
    ),
):
    try:
        vaccine = usecase.execute(id, payload)
        content = {
            "message": f"Le vaccin '{vaccine.name}' a bien été modifié."
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


@vaccine_router.delete("/{id}")
@inject
def endpoint_usecase_delete_vaccine_by_id(
    id: int,
    usecase: DeleteVaccineUseCase = Depends(
        Provide[VaccineContainer.delete_vaccine_usecase]
    ),
):
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