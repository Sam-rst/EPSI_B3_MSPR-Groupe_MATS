from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.presentation.model.payload.create_continent_payload import CreateContinentPayload


class ContinentRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create(self, payload: CreateContinentPayload) -> ContinentEntity:
        pass

    @abstractmethod
    def update(self, payload) -> ContinentEntity:
        # TODO: Implement this payload
        pass

    @abstractmethod
    def delete(self, id: int) -> ContinentEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> ContinentEntity:
        pass

    @abstractmethod
    def find_all(self) -> List[ContinentEntity]:
        pass

    @abstractmethod
    def exists(self, id: int) -> bool:
        pass
