from fastapi import HTTPException, status
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.epidemic.domain.interface.epidemic_repository import (
    EpidemicRepository,
)
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddVaccineUseCase(BaseUseCase):
    def __init__(
        self, repository: VaccineRepository, epidemic_repository: EpidemicRepository
    ):
        super().__init__(repository)
        self._epidemic_repository = epidemic_repository

    @property
    def epidemic_repository(self) -> EpidemicRepository:
        return self._epidemic_repository

    def execute(self, payload: CreateVaccinePayload) -> VaccineEntity | VaccineModel:
        try:
            existing_vaccine = self.repository.find_by_name(payload.name)
            if existing_vaccine:
                if not existing_vaccine.is_deleted:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le nom du vaccin existe déjà",
                    )
                else:
                    # Si le vaccin existe mais est supprimé, on le restaure
                    self.repository.reactivate(existing_vaccine)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le vaccin existe déjà, il a été supprimé mais il vient d'être restauré.",
                    )
            existing_epidemic = self.epidemic_repository.find_by_id(
                payload.epidemic_id
            )
            if not existing_epidemic:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="L'épidémie n'existe pas, veuillez en choisir une autre.",
                )

            return self.repository.create(payload)

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
