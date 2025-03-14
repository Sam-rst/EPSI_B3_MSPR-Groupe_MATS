from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.entity.base_entity import BaseEntity


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self):
        self._data = []

    @abstractmethod
    def create(self, entity: BaseEntity) -> BaseEntity:
        pass

    @abstractmethod
    def update(self, entity: BaseEntity) -> BaseEntity:
        pass

    @abstractmethod
    def delete(self, entity: BaseEntity) -> BaseEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> BaseEntity:
        pass

    @abstractmethod
    def find_all(self) -> List[BaseEntity]:
        pass

    @abstractmethod
    def exists(self, id: int) -> bool:
        pass
