from fastapi import HTTPException, status
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindCountryByIdUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self, id: int) -> CountryEntity:
        country = self.repository.find_by_id(id)

        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le country n’existe pas"
            )
        if country.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le country a été supprimé"
            )
        
        return country