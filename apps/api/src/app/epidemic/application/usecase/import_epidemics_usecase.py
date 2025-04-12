from fastapi import HTTPException, status
from src.app.epidemic.presentation.model.payload.create_epidemic_payload import (
    CreateEpidemicPayload,
)
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.epidemic.presentation.model.dto.bulk_insert_epidemics_response_dto import (
    BulkInsertEpidemicsErrorItemDTO,
    BulkInsertEpidemicsResponseDTO,
    BulkInsertEpidemicsSuccessItemDTO,
)


class ImportEpidemicsUseCase(BaseUseCase):
    def __init__(self, repository: EpidemicRepository):
        super().__init__(repository)

    def execute(
        self, payloads: list[CreateEpidemicPayload]
    ) -> BulkInsertEpidemicsResponseDTO:
        try:
            success = []
            errors = []
            for payload in payloads:
                existing_epidemic = self.repository.find_by_name(payload.name)
                if existing_epidemic:
                    if not existing_epidemic.is_deleted:
                        # Si l'epidemic existe et n'est pas supprimé, on l'ajoute à la liste des erreurs
                        errors.append(
                            BulkInsertEpidemicsErrorItemDTO(
                                name=payload.name,
                                error="Le nom de l'epidemic existe déjà",
                            )
                        )
                    else:
                        # Si l'epidemic existe mais est supprimé, on le restaure
                        self.repository.reactivate(existing_epidemic)
                        success.append(
                            BulkInsertEpidemicsSuccessItemDTO(
                                name=payload.name,
                                status="reactivated",
                            )
                        )
                else:
                    # Si l'epidemic n'existe pas, on le crée
                    self.repository.create(payload)
                    success.append(
                        BulkInsertEpidemicsSuccessItemDTO(
                            name=payload.name,
                            status="created",
                        )
                    )
            return BulkInsertEpidemicsResponseDTO(
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
