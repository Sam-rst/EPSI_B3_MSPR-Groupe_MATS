from abc import ABC, abstractmethod
from typing import List
from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.user.infrastructure.model.user_model import UserModel


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        self._data: List[UserEntity] = []

    @property
    def data(self) -> List[UserEntity]:
        return self._data

    @abstractmethod
    def create(
        self, user: UserEntity | UserModel
    ) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def update(
        self, user: UserEntity | UserModel
    ) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def delete(
        self, user: UserEntity | UserModel
    ) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity | UserModel:
        pass

    @abstractmethod
    def find_all(self) -> List[UserEntity] | List[UserModel]:
        pass

    @abstractmethod
    def reactivate(
        self, user: UserEntity | UserModel
    ) -> UserEntity | UserModel:
        pass