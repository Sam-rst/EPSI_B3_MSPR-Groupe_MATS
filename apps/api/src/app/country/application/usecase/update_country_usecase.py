from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.presentation.model.payload.update_country_payload import UpdateCountryPayload
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status

class UpdateCountryUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self, id: int, payload: UpdateCountryPayload) -> CountryEntity:
        country = self.repository.find_by_id(id)
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le country n'existe pas"
            )
        if country.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le country a été supprimé"
            )
        
        if payload.name is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nom ne peut pas être vide"
            )
        if payload.code3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le code ne peut pas être vide"
            )
        if payload.population is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La population ne peut pas être vide"
            )
        self.repository.update(country, payload)
        return country