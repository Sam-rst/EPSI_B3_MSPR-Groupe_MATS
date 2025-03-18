from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.infrastructure.model.base_model import BaseModel


class BaseMappingUtils:
    @staticmethod
    def entity_to_model(entity: BaseEntity) -> BaseModel:
        model = BaseModel(
            created_by=entity.created_by,
            updated_by=entity.updated_by
        )
        return model

    @staticmethod
    def model_to_entity(model: BaseModel) -> BaseEntity:
        entity = BaseEntity(
            created_by=model.created_by,
            updated_by=model.updated_by
        )
        return entity
