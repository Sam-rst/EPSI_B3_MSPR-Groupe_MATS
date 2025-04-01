from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.infrastructure.utils.vaccine_mapping_utils import (
    VaccineMappingUtils,
)
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)


class VaccineRepositoryInPostgres(VaccineRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateVaccinePayload) -> VaccineEntity:
        """
        Crée un vaccin dans la base de données.

        Args:
            payload (CreateVaccinePayload): Les données pour créer un vaccin.

        Returns:
            VaccineEntity: L'entité après insertion.
        """
        entity = VaccineEntity(
            name=payload.name,
            created_at=payload.created_at,
            created_by=payload.created_by,
        )
        model = VaccineMappingUtils.entity_to_model(entity)
        self.session.add(model)
        self.session.commit()
        return entity

    def update(self, id: int, payload: UpdateVaccinePayload) -> Optional[VaccineEntity]:
        """
        Met à jour un vaccin dans la base de données.

        Args:
            id (int): L'ID du vaccin à mettre à jour.
            payload (UpdateVaccinePayload): Les données pour mettre à jour le vaccin.

        Returns:
            Optional[VaccineEntity]: L'entité après mise à jour ou None si non trouvée.
        """
        model = self.session.query(VaccineModel).filter(VaccineModel.id == id).first()
        if not model:
            return None  # Le vaccin n'existe pas

        # Mise à jour des champs
        model.name = payload.name
        model.updated_at = payload.updated_at
        model.updated_by = payload.updated_by

        self.session.commit()
        return VaccineMappingUtils.model_to_entity(model)

    def delete(self, id: int) -> Optional[VaccineEntity]:
        """
        Supprime un vaccin de la base de données.

        Args:
            id (int): L'ID du vaccin à supprimer.

        Returns:
            Optional[VaccineEntity]: L'entité supprimée ou None si non trouvée.
        """
        model = self.session.query(VaccineModel).filter(VaccineModel.id == id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return VaccineMappingUtils.model_to_entity(model)
        return None

    def find_by_id(self, id: int) -> Optional[VaccineEntity]:
        """
        Recherche un vaccin par son ID.

        Args:
            id (int): L'ID du vaccin.

        Returns:
            Optional[VaccineEntity]: L'entité trouvée ou None.
        """
        model = self.session.query(VaccineModel).filter(VaccineModel.id == id).first()
        if model:
            return VaccineMappingUtils.model_to_entity(model)
        return None

    def find_by_name(self, name: str) -> Optional[VaccineEntity]:
        """
        Recherche un vaccin par son nom.

        Args:
            name (str): Le nom du vaccin.

        Returns:
            Optional[VaccineEntity]: L'entité trouvée ou None si non trouvée.
        """
        model = self.session.query(VaccineModel).filter(VaccineModel.name == name).first()
        if model:
            return VaccineMappingUtils.model_to_entity(model)
        return None

    def find_all(self) -> List[VaccineEntity]:
        """
        Récupère tous les vaccins de la base de données.

        Returns:
            List[VaccineEntity]: Liste des vaccins.
        """
        models = self.session.query(VaccineModel).all()
        return [VaccineMappingUtils.model_to_entity(model) for model in models]

    def exists(self, id: int) -> bool:
        """
        Vérifie si un vaccin existe dans la base de données.

        Args:
            id (int): L'ID du vaccin.

        Returns:
            bool: True si le vaccin existe, False sinon.
        """
        return self.session.query(VaccineModel).filter(VaccineModel.id == id).count() > 0