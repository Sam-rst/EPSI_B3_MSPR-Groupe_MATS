from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import UpdateVaccinePayload
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status


class UpdateVaccineUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository):
        super().__init__(repository)

    def execute(self, id: int, payload: UpdateVaccinePayload) -> VaccineEntity:
        # Recherche le vaccin par son ID
        vaccine = self.repository.find_by_id(id)
        if not vaccine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le vaccin n'existe pas"
            )
        if vaccine.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le vaccin a été supprimé"
            )

        # Vérification des champs obligatoires
        if payload.name is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nom ne peut pas être vide"
            )

        # Mise à jour du vaccin
        self.repository.update(vaccine, payload)
        return vaccine