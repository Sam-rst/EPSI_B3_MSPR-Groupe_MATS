from src.app.base.infrastructure.utils.base_mapping_utils import BaseMappingUtils
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel


class VaccineMappingUtils(BaseMappingUtils):
    @staticmethod
    def entity_to_model(entity: VaccineEntity) -> VaccineModel:
        """
        Convertit une entité VaccineEntity en modèle VaccineModel.

        Args:
            entity (VaccineEntity): L'entité à convertir.

        Returns:
            VaccineModel: Le modèle correspondant.
        """
        model = VaccineModel(
            name=entity.name,
            created_at=entity._created_at,
            created_by=entity._created_by,
            updated_at=entity._updated_at,
            updated_by=entity._updated_by,
        )
        return model

    @staticmethod
    def model_to_entity(model: VaccineModel) -> VaccineEntity:
        """
        Convertit un modèle VaccineModel en entité VaccineEntity.

        Args:
            model (VaccineModel): Le modèle à convertir.

        Returns:
            VaccineEntity: L'entité correspondante.
        """
        entity = VaccineEntity(
            name=model.name,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )
        entity._id = model.id  # Associe l'ID du modèle à l'entité
        return entity