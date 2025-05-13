from fastapi import HTTPException, status
from typing import List

from src.app.base.application.usecase.base_usecase import BaseUseCase


class ExportDataForMachineLearningUseCase(BaseUseCase):
    def __init__(self, repository: None): # TODO : Apporter le bon type de repository
        super().__init__(repository)

    def execute(self) -> None: # TODO : Apporter le bon type de retour
        try:
            # TODO : Aporter toute la logique pour exporter les données
            return None

        except HTTPException as http_exc:
            # On relance les erreurs HTTP explicites (404, 400, etc.)
            raise HTTPException(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue: {str(e)}",
            )