from abc import ABC, abstractmethod
from typing import List
from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.role.domain.entity.role_entity import RoleEntity
from src.app.role.infrastructure.model.role_model import RoleModel


class RoleRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        self._data: List[RoleEntity] = []

    @property
    def data(self) -> List[RoleEntity]:
        return self._data

    @abstractmethod
    def create(
        self, role: RoleEntity | RoleModel
    ) -> RoleEntity | RoleModel:
        pass

    @abstractmethod
    def update(
        self, role: RoleEntity | RoleModel
    ) -> RoleEntity | RoleModel:
        pass

    @abstractmethod
    def delete(
        self, role: RoleEntity | RoleModel
    ) -> RoleEntity | RoleModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> RoleEntity | RoleModel:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> RoleEntity | RoleModel:
        pass

    @abstractmethod
    def find_all(self) -> List[RoleEntity] | List[RoleModel]:
        pass

    @abstractmethod
    def reactivate(
        self, role: RoleEntity | RoleModel
    ) -> RoleEntity | RoleModel:
        pass