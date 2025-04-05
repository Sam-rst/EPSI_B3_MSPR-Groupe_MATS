from fastapi import HTTPException, status
from typing import List

from src.app.epidemic.domain.entity.epidemic_entity import EpidemicEntity
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllEpidemicsUseCase(BaseUseCase):
    def __init__(self, repository: EpidemicRepository):
        super().__init__(repository)

    def execute(self) -> List[EpidemicEntity] | List[EpidemicModel]:
        try:
            epidemics = self.repository.find_all()
            return epidemics

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