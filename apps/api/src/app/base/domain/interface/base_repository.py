from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.infrastructure.model.base_model import BaseModel


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self):
        self._data = []

    @abstractmethod
    def create(self, base: BaseEntity | BaseModel) -> BaseEntity | BaseModel:
        pass

    @abstractmethod
    def update(self, base: BaseEntity | BaseModel) -> BaseEntity | BaseModel:
        pass

    @abstractmethod
    def delete(self, base: BaseEntity | BaseModel) -> BaseEntity | BaseModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> BaseEntity | BaseModel:
        pass

    @abstractmethod
    def find_all(self) -> List[BaseEntity] | List[BaseModel]:
        pass

    @abstractmethod
    def reactivate(self, base: BaseEntity | BaseModel) -> BaseEntity | BaseModel:
        pass
