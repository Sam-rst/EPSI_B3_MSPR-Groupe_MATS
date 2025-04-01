from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.presentation.model.payload.update_continent_payload import UpdateContinentPayload
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from fastapi import HTTPException, status

class UpdateContinentUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self, id: int, payload: UpdateContinentPayload) -> ContinentEntity:
        continent = self.repository.find_by_id(id)
        if not continent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le continent n'existe pas"
            )
        if continent.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le continent a été supprimé"
            )
        
        if payload.name is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nom ne peut pas être vide"
            )
        if payload.code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le code ne peut pas être vide"
            )
        if payload.population is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La population ne peut pas être vide"
            )
        self.repository.update(continent, payload)
        return continent