from fastapi import HTTPException, status
from typing import List

from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllVaccinesUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository):
        super().__init__(repository)

    def execute(self) -> List[VaccineEntity] | List[VaccineModel]:
        try:
            vaccines = self.repository.find_all()
            return vaccines

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