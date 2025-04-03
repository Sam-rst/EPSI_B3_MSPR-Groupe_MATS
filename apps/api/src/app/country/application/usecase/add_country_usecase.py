from fastapi import HTTPException, status
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddCountryUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

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
                    existing_country.is_deleted = False
                    self.repository.update(existing_country)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le code iso3 existe sur un pays supprimé, le pays a été réactivé veuillez utiliser la requête PATCH pour modifier",
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
