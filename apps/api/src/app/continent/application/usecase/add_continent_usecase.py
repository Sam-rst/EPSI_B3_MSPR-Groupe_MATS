from fastapi import HTTPException, status
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddContinentUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(
        self, payload: CreateContinentPayload
    ) -> ContinentEntity | ContinentModel:
        try:
            existing_continent = self.repository.find_by_code(payload.code)
            if existing_continent:
                if not existing_continent.is_deleted:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le code continent existe déjà",
                    )
                else:
                    existing_continent.is_deleted = False
                    self.repository.update(existing_continent)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le code existe sur un continent supprimé, le continent a été réactivé veuillez utiliser la requête PATCH pour modifier",
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
