from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.infrastructure.utils.continent_mapping_utils import (
    ContinentMappingUtils,
)
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)


class ContinentRepositoryInPostgres(ContinentRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.

        Args:
            session (Session): La session SQLAlchemy pour interagir avec la base de données.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateContinentPayload) -> ContinentEntity:
        """
        Crée un continent dans la base de données.

        Args:
            entity (ContinentModel): L'entité du continent à insérer.

        Returns:
            ContinentModel: L'entité après insertion.
        """

        entity = ContinentEntity(
            name=payload.name, code=payload.code, population=payload.population
        )
        model = ContinentMappingUtils.entity_to_model(entity)
        self.session.add(model)
        self.session.commit()
        return entity

    def update(self, id: int, payload: CreateContinentPayload) -> ContinentEntity:
        """
        Met à jour un continent dans la base de données.

        Args:
            entity (ContinentModel): L'entité à mettre à jour.

        Returns:
            ContinentModel: L'entité après mise à jour.
        """
        # TODO : Changer le payload par l'autre payload d'update
        pass

    def delete(self, id: int) -> ContinentEntity:
        """
        Supprime un continent de la base de données.

        Args:
            entity (ContinentModel): L'entité à supprimer.

        Returns:
            ContinentModel: L'entité supprimée.
        """
        entity = self.find_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return entity
        # TODO : Gérer l'erreur
        return None

    def find_by_id(self, id: int) -> Optional[ContinentEntity]:
        """
        Recherche un continent par son ID.

        Args:
            id (int): L'ID du continent.

        Returns:
            Optional[ContinentModel]: L'entité trouvée ou None.
        """
        model = self.session.query(ContinentModel).filter(ContinentModel.id == id).first()
        if model:
            return ContinentMappingUtils.model_to_entity(model)
        # TODO : Gérer l'erreur
        return None

    def find_all(self) -> List[ContinentModel]:
        """
        Récupère tous les continents de la base de données.

        Returns:
            List[ContinentModel]: Liste des continents.
        """
        return self.session.query(ContinentModel).all()

    def exists(self, id: int) -> bool:
        """
        Vérifie si un continent existe dans la base de données.

        Args:
            id (int): L'ID du continent.

        Returns:
            bool: True si le continent existe, False sinon.
        """
        pass
