from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.infrastructure.model.base_model import BaseModel


class BaseMappingUtils:
    @staticmethod
    def entity_to_model(entity: BaseEntity) -> BaseModel:
        model = BaseModel(
            id=entity.id,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
            deleted_at=entity.deleted_at,
            deleted_by=entity.deleted_by,
            is_deleted=entity.is_deleted
        )
        return model

    @staticmethod
    def model_to_entity(model: BaseModel) -> BaseEntity:
        entity = BaseEntity(
            id=model.id,
            created_by=model.created_by,
            updated_by=model.updated_by
        )
        entity._created_at = model.created_at
        entity._updated_at = model.updated_at
        entity._deleted_at = model.deleted_at
        entity._deleted_by = model.deleted_by
        entity._is_deleted = model.is_deleted
        return entity
