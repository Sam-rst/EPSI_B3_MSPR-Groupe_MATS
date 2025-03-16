from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.presentation.model.payload.find_continent_by_id_payload import (
    FindContinentByIdPayload,
)
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindContinentByIdUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self, payload: FindContinentByIdPayload) -> ContinentEntity:
        continent = self.repository.find_by_id(payload.id)
        
        if not continent:
            raise ValueError("Le continent n’existe pas")
        
        if continent.is_deleted:
            raise ValueError("Le continent a été supprimé")
        
        return continent