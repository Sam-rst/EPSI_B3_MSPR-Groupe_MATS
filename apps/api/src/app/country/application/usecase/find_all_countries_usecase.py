from fastapi import HTTPException, status
from typing import List

from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllCountriesUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self) -> List[CountryEntity] | List[CountryModel]:
        try:
            countries = self.repository.find_all()
            return countries

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