from fastapi import HTTPException, status
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.continent.domain.interface.continent_repository import (
    ContinentRepository,
)
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.country.presentation.model.dto.bulk_insert_countries_response_dto import (
    BulkInsertCountriesErrorItemDTO,
    BulkInsertCountriesResponseDTO,
    BulkInsertCountriesSuccessItemDTO,
)


class ImportCountriesUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository, continent_repository):
        super().__init__(repository)
        self._continent_repository = continent_repository

    @property
    def continent_repository(self) -> ContinentRepository:
        return self._continent_repository

    def execute(
        self, payloads: list[CreateCountryPayload]
    ) -> BulkInsertCountriesResponseDTO:
        try:
            success = []
            errors = []
            for payload in payloads:
                existing_country = self.repository.find_by_iso3(payload.iso3)
                if existing_country:
                    if not existing_country.is_deleted:
                        # Si le pays existe et n'est pas supprimé, on l'ajoute à la liste des erreurs
                        errors.append(
                            BulkInsertCountriesErrorItemDTO(
                                iso3=payload.iso3,
                                error="Le nom du pays existe déjà",
                            )
                        )
                    else:
                        # Si le pays existe mais est supprimé, on le restaure
                        self.repository.reactivate(existing_country)
                        success.append(
                            BulkInsertCountriesSuccessItemDTO(
                                iso3=payload.iso3,
                                status="reactivated",
                            )
                        )
                else:
                    existing_continent = self.continent_repository.find_by_id(
                        payload.continent_id
                    )
                    if not existing_continent:
                        errors.append(
                            BulkInsertCountriesErrorItemDTO(
                                iso3=payload.iso3,
                                error="Le continent n'existe pas, veuillez en choisir un autre.",
                            )
                        )
                    else:
                        # Si le pays n'existe pas, on le crée
                        self.repository.create(payload)
                        success.append(
                            BulkInsertCountriesSuccessItemDTO(
                                iso3=payload.iso3,
                                status="created",
                            )
                        )
            return BulkInsertCountriesResponseDTO(
                success=success,
                errors=errors,
            )

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
