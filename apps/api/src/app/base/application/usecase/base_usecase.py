from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.domain.interface.base_repository import BaseRepository


class BaseUseCase:
    def __init__(self, repository: BaseRepository):
        self._repository = repository

    @property
    def repository(self) -> BaseRepository:
        return self._repository

    @repository.setter
    def repository(self, value: BaseRepository):
        self._repository = value
