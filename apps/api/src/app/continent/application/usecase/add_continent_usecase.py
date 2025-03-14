from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.presentation.model.payload.create_continent_pauload import (
    CreateContinentPayload,
)
from src.app.continent.domain.interface.continent_repository import ContinentRepository


class AddContinentUseCase:
    def __init__(self, repository: ContinentRepository):
        self._repository = repository

    @property
    def repository(self) -> ContinentRepository:
        return self._repository

    @repository.setter
    def repository(self, value: ContinentRepository):
        self._repository = value

    def execute(self, payload: CreateContinentPayload) -> ContinentEntity:
        continentCreated = ContinentEntity(
            name=payload.name, code=payload.code, population=payload.population
        )
        return self.repository.create(continentCreated)
