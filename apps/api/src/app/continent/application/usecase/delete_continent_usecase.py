from datetime import datetime
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status


class DeleteContinentUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self, id: int) -> ContinentEntity | ContinentModel:
        continent = self.repository.find_by_id(id)
        if not continent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le continent n'existe pas",
            )
        if continent.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le continent a déjà été supprimé",
            )

        return self.repository.delete(continent)
