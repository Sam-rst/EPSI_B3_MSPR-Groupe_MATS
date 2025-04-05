from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.presentation.model.payload.update_continent_payload import (
    UpdateContinentPayload,
)


class ContinentRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create(self, payload: CreateContinentPayload) -> ContinentEntity | ContinentModel:
        pass

    @abstractmethod
    def update(
        self,
        continent: ContinentEntity | ContinentModel,
        payload: UpdateContinentPayload,
    ) -> ContinentEntity | ContinentModel:
        pass

    @abstractmethod
    def delete(self, continent: ContinentEntity | ContinentModel) -> ContinentEntity | ContinentModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> ContinentEntity | ContinentModel:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> ContinentEntity | ContinentModel:
        pass

    @abstractmethod
    def find_all(self) -> List[ContinentEntity] | List[ContinentModel]:
        pass

    @abstractmethod
    def reactivate(self, continent: ContinentEntity | ContinentModel) -> ContinentEntity | ContinentModel:
        pass
