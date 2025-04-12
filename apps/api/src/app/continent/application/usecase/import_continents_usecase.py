from fastapi import HTTPException, status
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.continent.presentation.model.dto.bulk_insert_continents_response_dto import BulkInsertResponseDTO, BulkInsertErrorItemDTO, BulkInsertSuccessItemDTO

class ImportContinentsUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(
        self, payloads: list[CreateContinentPayload]
    ) -> BulkInsertResponseDTO:
        try:
            success = []
            errors = []
            for payload in payloads:
                existing_continent = self.repository.find_by_code(payload.code)
                if existing_continent:
                    if not existing_continent.is_deleted:
                        # Si le continent existe et n'est pas supprimé, on l'ajoute à la liste des erreurs
                        errors.append(
                            BulkInsertErrorItemDTO(
                                code=payload.code,
                                error="Le code continent existe déjà",
                            )
                        )
                    else:
                        # Si le continent existe mais est supprimé, on le restaure
                        self.repository.reactivate(existing_continent)
                        success.append(
                            BulkInsertSuccessItemDTO(
                                code=payload.code,
                                status="reactivated",
                            )
                        )
                else:
                    # Si le continent n'existe pas, on le crée
                    self.repository.create(payload)
                    success.append(
                        BulkInsertSuccessItemDTO(
                            code=payload.code,
                            status="created",
                        )
                    )
            return BulkInsertResponseDTO(
                success=success,
                errors=errors,
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
