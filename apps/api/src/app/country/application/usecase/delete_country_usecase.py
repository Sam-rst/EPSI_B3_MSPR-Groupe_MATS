from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status


class DeleteCountryUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self, id: int) -> CountryEntity | CountryModel:
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
                    detail="Le pays a déjà été supprimé",
                )

            return self.repository.delete(country)

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
