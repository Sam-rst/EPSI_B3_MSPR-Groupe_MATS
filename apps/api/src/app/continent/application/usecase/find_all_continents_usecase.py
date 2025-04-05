from fastapi import HTTPException, status
from typing import List

from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllContinentsUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self) -> List[ContinentEntity] | List[ContinentModel]:
        try:
            continents = self.repository.find_all()
            return continents

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
