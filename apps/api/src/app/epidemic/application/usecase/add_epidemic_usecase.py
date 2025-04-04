from fastapi import HTTPException, status
from src.app.epidemic.domain.entity.epidemic_entity import EpidemicEntity
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.epidemic.presentation.model.payload.create_epidemic_payload import (
    CreateEpidemicPayload,
)
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddEpidemicUseCase(BaseUseCase):
    def __init__(self, repository: EpidemicRepository):
        super().__init__(repository)

    def execute(self, payload: CreateEpidemicPayload) -> EpidemicEntity | EpidemicModel:
        try:
            existing_epidemic = self.repository.find_by_name(payload.name)
            if existing_epidemic:
                if not existing_epidemic.is_deleted:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le nom de cette épidémie existe déjà",
                    )
                else:
                    # Si le pays existe mais est supprimé, on le restaure
                    self.repository.reactivate(existing_epidemic)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="L'épidémie existe déjà, il a été supprimé mais il vient d'être restauré.",
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
