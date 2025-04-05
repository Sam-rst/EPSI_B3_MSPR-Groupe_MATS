from src.app.epidemic.domain.entity.epidemic_entity import EpidemicEntity
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.epidemic.presentation.model.payload.update_epidemic_payload import (
    UpdateEpidemicPayload,
)
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status


class UpdateEpidemicUseCase(BaseUseCase):
    def __init__(
        self, repository: EpidemicRepository):
        super().__init__(repository)

    def execute(
        self, id: int, payload: UpdateEpidemicPayload
    ) -> EpidemicEntity | EpidemicModel:
        try:
            epidemic = self.repository.find_by_id(id)
            if not epidemic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="L'épidémie n'existe pas",
                )
            if epidemic.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="L'épidémie a été supprimée",
                )

            self.repository.update(epidemic, payload)
            return epidemic

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
