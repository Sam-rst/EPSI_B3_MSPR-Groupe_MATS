from fastapi import HTTPException, status
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.continent.domain.interface.continent_repository import (
    ContinentRepository,
)
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddCountryUseCase(BaseUseCase):
    def __init__(
        self, repository: CountryRepository, continent_repository: ContinentRepository
    ):
        super().__init__(repository)
        self._continent_repository = continent_repository

    @property
    def continent_repository(self) -> ContinentRepository:
        return self._continent_repository

    def execute(self, payload: CreateCountryPayload) -> CountryEntity | CountryModel:
        try:
            existing_country = self.repository.find_by_iso3(payload.iso3)
            if existing_country:
                if not existing_country.is_deleted:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le code iso3 existe déjà",
                    )
                else:
                    # Si le pays existe mais est supprimé, on le restaure
                    self.repository.reactivate(existing_country)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le pays existe déjà, il a été supprimé mais il vient d'être restauré.",
                    )
            existing_continent = self.continent_repository.find_by_id(
                payload.continent_id
            )
            if not existing_continent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le continent n'existe pas, veuillez en choisir un autre.",
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
