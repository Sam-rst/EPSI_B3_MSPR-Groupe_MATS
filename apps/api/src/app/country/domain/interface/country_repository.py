from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.country.domain.entity.country_entity import CountryEntity


class CountryRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        self._data: List[CountryEntity] = []

    @property
    def data(self) -> List[CountryEntity]:
        return self._data

    @abstractmethod
    def create(self, entity: CountryEntity) -> CountryEntity:
        pass

    @abstractmethod
    def update(self, entity: CountryEntity) -> CountryEntity:
        pass

    @abstractmethod
    def delete(self, entity: CountryEntity) -> CountryEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> CountryEntity:
        pass

    @abstractmethod
    def find_all(self) -> List[CountryEntity]:
        pass

    @abstractmethod
    def exists(self, id: int) -> bool:
        pass
