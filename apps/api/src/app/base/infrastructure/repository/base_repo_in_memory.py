from typing import List
from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.base.infrastructure.utils.base_mapping_utils import BaseMappingUtils

class BaseRepositoryInMemory(BaseRepository):
    def __init__(self):
        self._data = []

    def create(self, entity: BaseEntity) -> BaseEntity:
        model = BaseMappingUtils.domain_to_model(entity)
        self._data.append(model)
        return BaseMappingUtils.model_to_domain(model)

    def update(self, entity: BaseEntity) -> BaseEntity:
        for index, model in enumerate(self._data):
            if model.id == entity.id:
                self._data[index] = BaseMappingUtils.domain_to_model(entity)
                return BaseMappingUtils.model_to_domain(self._data[index])
        return None

    def delete(self, entity: BaseEntity) -> BaseEntity:
        for index, model in enumerate(self._data):
            if model.id == entity.id:
                del self._data[index]
                return entity
        return None

    def find_by_id(self, id: int) -> BaseEntity:
        for model in self._data:
            if model.id == id:
                return BaseMappingUtils.model_to_domain(model)
        return None

    def find_all(self) -> List[BaseEntity]:
        return [BaseMappingUtils.model_to_domain(model) for model in self._data]

    def exists(self, id: int) -> bool:
        return any(model.id == id for model in self._data)