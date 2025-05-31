import csv
import io
from typing import List, Dict, Any, Union, TypeAlias

from fastapi import HTTPException, status
from typing import List

from src.config.models import MODEL_REGISTRY
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.machine_learning.domain.interface.machine_learning_repository import (
    MachineLearningRepository,
)
from src.app.base.presentation.model.payload.base_payload import FilterRequest


class ExportDataForMachineLearningUseCase(BaseUseCase):
    def __init__(self, repository: MachineLearningRepository):
        super().__init__(repository)

    def validate_filter(self, f):
        """Valide un filtre et retourne les informations nécessaires pour l'appliquer."""
        Model = MODEL_REGISTRY.get(f.model)
        if not Model:
            raise HTTPException(
                status_code=400,
                detail=f"Modèle inconnu dans les filtres: {f.model}",
            )

        column = getattr(Model, f.column, None)
        if not column:
            raise HTTPException(
                status_code=400,
                detail=f"Champ inconnu dans les filtres: {f.column}",
            )

        # Validation des opérateurs spéciaux
        if f.operator == "in":
            if not isinstance(f.value, list):
                raise HTTPException(
                    status_code=400,
                    detail="L'opérateur 'in' nécessite une liste de valeurs",
                )
        elif f.operator == "between":
            if not isinstance(f.value, list) or len(f.value) != 2:
                raise HTTPException(
                    status_code=400,
                    detail="L'opérateur 'between' nécessite une liste de 2 valeurs [min, max]",
                )
        elif f.operator not in ["=", "!=", "<", "<=", ">", ">=", "like"]:
            raise HTTPException(
                status_code=400,
                detail=f"Opérateur non supporté: {f.operator}",
            )

        return Model, column

    def execute(self, payload: FilterRequest) -> bytes:
        try:
            # Validation des filtres
            for f in payload.filters:
                if f.label:
                    if not self.repository.check_label_in_table_statistic(f.label):
                        raise HTTPException(
                            status_code=400,
                            detail=f"Label inconnu dans les filtres: {f.label}",
                        )
                else:
                    self.validate_filter(f)

            # Validation des colonnes
            if payload.columns:
                for c in payload.columns:
                    Model = MODEL_REGISTRY.get(c.model)
                    if not Model:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Modèle inconnu dans les colonnes: {c.model}",
                        )
                    column = getattr(Model, c.column, None)
                    if not column:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Champ inconnu dans les colonnes: {c.column}",
                        )

            # Validation du tri
            if payload.sort:
                Model = MODEL_REGISTRY.get(payload.sort.model)
                if not Model:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Modèle inconnu dans le sort: {payload.sort.model}",
                    )
                column = getattr(Model, payload.sort.column, None)
                if not column:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Champ inconnu dans le sort: {payload.sort.column}",
                    )

            data = self.repository.get_data(payload)

            if not data:
                raise HTTPException(
                    status_code=400,
                    detail="Aucune donnée trouvée",
                )
            # Convertir les résultats dans un format compatible avec le machine learning en fichier csv
            output = io.StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow(data[0].keys())  # Écriture des en-têtes
            for row in data:
                csv_writer.writerow(row.values())  # Écriture des données

            # Convertir la chaîne en bytes
            return output.getvalue().encode("utf-8")

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
