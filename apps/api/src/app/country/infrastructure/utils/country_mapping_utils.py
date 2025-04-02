from src.app.base.infrastructure.utils.base_mapping_utils import BaseMappingUtils
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel


class CountryMappingUtils(BaseMappingUtils):
    @staticmethod
    def entity_to_model(entity: CountryEntity) -> CountryModel:
        model = CountryModel(
            name=entity.name,
            iso2=entity.iso2,
            iso3=entity.iso3,
            code3=entity.code3,
            population=entity.population,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
        )
        return model

    @staticmethod
    def model_to_entity(model: CountryModel) -> CountryEntity:
        entity = CountryEntity(
            name=model.name,
            iso2=model.iso2,
            iso3=model.iso3,
            code3=model.code3,
            population=model.population
        )
        entity._created_at = model.created_at
        entity._updated_at = model.updated_at
        entity._deleted_at = model.deleted_at
        entity._deleted_by = model.deleted_by
        entity._is_deleted = model.is_deleted
        return entity