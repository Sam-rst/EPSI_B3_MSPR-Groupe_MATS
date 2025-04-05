from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.presentation.model.payload.update_country_payload import (
    UpdateCountryPayload,
)
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status


class UpdateCountryUseCase(BaseUseCase):
    def __init__(
        self, repository: CountryRepository, continent_repository: ContinentRepository
    ):
        super().__init__(repository)
        self._continent_repository = continent_repository

    @property
    def continent_repository(self) -> ContinentRepository:
        return self._continent_repository

    def execute(
        self, id: int, payload: UpdateCountryPayload
    ) -> CountryEntity | CountryModel:
        try:
            country = self.repository.find_by_id(id)
            if not country:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Le pays n'existe pas",
                )
            if country.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le pays a été supprimé",
                )

            continent = self.continent_repository.find_by_id(payload.continent_id)
            if not continent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Le continent n'existe pas, veuillez choisir un autre continent",
                )
            if continent.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le continent a été supprimé, veuillez choisir un autre continent",
                )

            self.repository.update(country, payload)
            return country

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
