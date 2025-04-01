from fastapi import HTTPException, status
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddVaccineUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository):
        super().__init__(repository)

    def execute(self, payload: CreateVaccinePayload) -> VaccineEntity:
        # Vérifie si un vaccin avec le même nom existe déjà
        existing_vaccine = self.repository.find_by_name(payload.name)
        if existing_vaccine:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un vaccin avec ce nom existe déjà"
            )

        # Crée un nouveau vaccin
        return self.repository.create(payload)