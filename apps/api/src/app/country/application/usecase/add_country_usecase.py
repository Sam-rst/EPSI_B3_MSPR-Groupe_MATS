from fastapi import HTTPException, status
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddCountryUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self, payload: CreateCountryPayload) -> CountryEntity:
        existing_country = self.repository.find_by_code3(payload.code3)
        if existing_country:
            if not existing_country.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le code country existe déjà"
                )
            else:
                existing_country.is_deleted = False
                self.repository.update(existing_country)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le code existe sur un country supprimé, le country a été réactivé veuillez utiliser la requête PATCH pour modifier"
                )
        return self.repository.create(payload)