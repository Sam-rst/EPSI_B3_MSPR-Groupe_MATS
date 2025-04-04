from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.epidemic.domain.entity.epidemic_entity import EpidemicEntity
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel


class EpidemicRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        self._data: List[EpidemicEntity] = []

    @property
    def data(self) -> List[EpidemicEntity]:
        return self._data

    @abstractmethod
    def create(
        self, epidemic: EpidemicEntity | EpidemicModel
    ) -> EpidemicEntity | EpidemicModel:
        pass

    @abstractmethod
    def update(
        self, epidemic: EpidemicEntity | EpidemicModel
    ) -> EpidemicEntity | EpidemicModel:
        pass

    @abstractmethod
    def delete(
        self, epidemic: EpidemicEntity | EpidemicModel
    ) -> EpidemicEntity | EpidemicModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> EpidemicEntity | EpidemicModel:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> EpidemicEntity | EpidemicModel:
        pass

    @abstractmethod
    def find_all(self) -> List[EpidemicEntity] | List[EpidemicModel]:
        pass

    @abstractmethod
    def reactivate(
        self, epidemic: EpidemicEntity | EpidemicModel
    ) -> EpidemicEntity | EpidemicModel:
        pass
