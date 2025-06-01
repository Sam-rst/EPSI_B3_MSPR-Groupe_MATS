import json
from typing import Dict
from fastapi import HTTPException, UploadFile, status
import pandas as pd

from src.app.base.application.usecase.base_usecase import BaseUseCase

from src.app.machine_learning.domain.interface.machine_learning_repository import (
    MachineLearningRepository,
)

class AskPredictionToMachineLearningUseCase(BaseUseCase):
    def __init__(self, repository: MachineLearningRepository):
        super().__init__(repository)

    def execute(self, file: UploadFile) -> Dict:
        """
        Demande des prédictions à partir d'un fichier CSV.

        Args:
            file (UploadFile): Le fichier CSV contenant les données pour la prédiction

        Returns:
            Dict: Les prédictions au format JSON

        Raises:
            HTTPException: Si le fichier n'est pas au format CSV ou si une erreur survient
        """
        try:
            # Vérifier le type MIME du fichier
            if not file.content_type == "text/csv":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le fichier doit être au format CSV",
                )

            # Lire le fichier CSV avec pandas
            try:
                df = pd.read_csv(file.file)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erreur lors de la lecture du CSV: {str(e)}",
                )

            # Obtenir les prédictions via le repository
            predictions = self.repository.get_predictions(file.file)

            # Convertir les prédictions en JSON
            try:
                predictions_json = json.dumps(predictions)
                return json.loads(predictions_json)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la conversion en JSON: {str(e)}",
                )

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