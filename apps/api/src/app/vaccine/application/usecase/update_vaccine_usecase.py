from fastapi import HTTPException, status
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository


class UpdateVaccineUseCase(BaseUseCase):
    def __init__(
        self, repository: VaccineRepository, epidemic_repository: EpidemicRepository
    ):
        super().__init__(repository)
        self._epidemic_repository = epidemic_repository

    @property
    def epidemic_repository(self) -> VaccineRepository:
        return self._epidemic_repository

    def execute(
        self, id: int, payload: UpdateVaccinePayload
    ) -> VaccineEntity | VaccineModel:
        try:
            vaccine = self.repository.find_by_id(id)
            if not vaccine:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Le vaccin n'existe pas",
                )
            if vaccine.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le vaccin a été supprimé",
                )

            epidemic = self.epidemic_repository.find_by_id(payload.epidemic_id)
            if not epidemic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="L'épidémie n'existe pas, veuillez choisir une autre épidémie",
                )
            if epidemic.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="L'épidémie a été supprimée, veuillez choisir une autre épidémie",
                )

            self.repository.update(vaccine, payload)
            return vaccine

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
