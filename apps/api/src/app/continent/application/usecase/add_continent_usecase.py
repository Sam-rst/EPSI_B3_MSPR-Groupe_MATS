from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.presentation.model.payload.create_continent_pauload import (
    CreateContinentPayload,
)
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddContinentUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self, payload: CreateContinentPayload) -> ContinentEntity:
        continentCreated = ContinentEntity(
            name=payload.name, code=payload.code, population=payload.population
        )
        return self.repository.create(continentCreated)
