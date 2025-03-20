from src.app.base.infrastructure.utils.base_mapping_utils import BaseMappingUtils
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel


class ContinentMappingUtils(BaseMappingUtils):
    @staticmethod
    def entity_to_model(entity: ContinentEntity) -> ContinentModel:
        model = ContinentModel(
            name=entity.name,
            code=entity.code,
            population=entity.population,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
        )
        return model

    @staticmethod
    def model_to_entity(model: ContinentModel) -> ContinentEntity:
        entity = ContinentEntity(
            name=model.name,
            code=model.code,
            population=model.population,
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
        return entity
