from fastapi import APIRouter, File, UploadFile, status, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from src.core.middlewares.limiter import limiter
from src.core.dependencies import get_current_user

# =====Containers=====
from src.app.machine_learning.container import MachineLearningContainer

# =====Usecases=====
from src.app.machine_learning.application.usecase.export_data_for_machine_learning_usecase import (
    ExportDataForMachineLearningUseCase,
)
from src.app.machine_learning.application.usecase.ask_prediction_to_machine_learning_usecase import (
    AskPredictionToMachineLearningUseCase,
)

# =====Payloads=====
from src.app.base.presentation.model.payload.base_payload import FilterRequest

# =====DTOs=====

machine_learning_router = APIRouter(
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


@machine_learning_router.post("/ask")
@limiter.limit("5/minute")
@inject
async def endpoint_ask_prediction_to_machine_learning(
    request: Request,
    file: UploadFile = File(...),
    usecase: AskPredictionToMachineLearningUseCase = Depends(
        Provide[MachineLearningContainer.ask_prediction_to_machine_learning_usecase]
    ),
):
    """
    Demande une prédiction au modèle de machine learning.

    Returns:
        JSONResponse: TODO : Décrire la réponse
    """
    try:
        content = await usecase.execute(file)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@machine_learning_router.post("/export")
@limiter.limit("5/minute")
@inject
def endpoint_export_data_for_machine_learning(
    request: Request,
    payload: FilterRequest,
    usecase: ExportDataForMachineLearningUseCase = Depends(
        Provide[MachineLearningContainer.export_data_for_machine_learning_usecase]
    ),
):
    """
    Export de donnée pour le modèle de machine learning.

    Returns:
        StreamingResponse: Fichier CSV contenant les données exportées
    """
    try:
        csv_content = usecase.execute(payload)
        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=export_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            },
        )
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"message": str(http_exc.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
