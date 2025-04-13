from fastapi import HTTPException, status
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.epidemic.domain.interface.epidemic_repository import (
    EpidemicRepository,
)
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.vaccine.presentation.model.dto.bulk_insert_vaccines_response_dto import (
    BulkInsertVaccinesErrorItemDTO,
    BulkInsertVaccinesResponseDTO,
    BulkInsertVaccinesSuccessItemDTO,
)


class ImportVaccinesUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository, epidemic_repository: EpidemicRepository):
        super().__init__(repository)
        self._epidemic_repository = epidemic_repository

    @property
    def epidemic_repository(self) -> EpidemicRepository:
        return self._epidemic_repository

    def execute(
        self, payloads: list[CreateVaccinePayload]
    ) -> BulkInsertVaccinesResponseDTO:
        try:
            success = []
            errors = []
            for payload in payloads:
                existing_vaccine = self.repository.find_by_name(payload.name)
                if existing_vaccine:
                    if not existing_vaccine.is_deleted:
                        # Si le vaccine existe et n'est pas supprimé, on l'ajoute à la liste des erreurs
                        errors.append(
                            BulkInsertVaccinesErrorItemDTO(
                                name=payload.name,
                                error="Le nom du vaccin existe déjà",
                            )
                        )
                    else:
                        # Si le vaccine existe mais est supprimé, on le restaure
                        self.repository.reactivate(existing_vaccine)
                        success.append(
                            BulkInsertVaccinesSuccessItemDTO(
                                name=payload.name,
                                status="reactivated",
                            )
                        )
                else:
                    existing_epidemic = self.epidemic_repository.find_by_id(
                        payload.epidemic_id
                    )
                    if not existing_epidemic:
                        errors.append(
                            BulkInsertVaccinesErrorItemDTO(
                                name=payload.name,
                                error="L'épidémie n'existe pas, veuillez en choisir une autre.",
                            )
                        )
                    else:
                        # Si le vaccine n'existe pas, on le crée
                        self.repository.create(payload)
                        success.append(
                            BulkInsertVaccinesSuccessItemDTO(
                                name=payload.name,
                                status="created",
                            )
                        )
            return BulkInsertVaccinesResponseDTO(
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
