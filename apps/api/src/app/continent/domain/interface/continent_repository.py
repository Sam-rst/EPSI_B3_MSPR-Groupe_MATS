from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity


class ContinentRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        self._data = []

    @abstractmethod
    def create(self, entity: ContinentEntity) -> ContinentEntity:
        pass

    @abstractmethod
    def update(self, entity: ContinentEntity) -> ContinentEntity:
        pass

    @abstractmethod
    def delete(self, entity: ContinentEntity) -> ContinentEntity:
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
