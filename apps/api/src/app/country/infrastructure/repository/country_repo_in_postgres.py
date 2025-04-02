from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.infrastructure.utils.country_mapping_utils import (
    CountryMappingUtils,
)
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.presentation.model.payload.update_country_payload import (
    UpdateCountryPayload,
)


class CountryRepositoryInPostgres(CountryRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateCountryPayload) -> CountryEntity:
        """
        Crée un pays dans la base de données.

        Args:
            payload (CreateCountryPayload): Les données pour créer un pays.

        Returns:
            CountryEntity: L'entité après insertion.
        """
        entity = CountryEntity(
            name=payload.name,
            iso2=payload.iso2,
            iso3=payload.iso3,
            code3=payload.code3,
            population=payload.population,
        )
        model = CountryMappingUtils.entity_to_model(entity)
        self.session.add(model)
        self.session.commit()
        return entity

    def update(self, id: int, payload: UpdateCountryPayload) -> Optional[CountryEntity]:
        """
        Met à jour un pays dans la base de données.

        Args:
            id (int): L'ID du pays à mettre à jour.
            payload (UpdateCountryPayload): Les données pour mettre à jour le pays.

        Returns:
            Optional[CountryEntity]: L'entité après mise à jour ou None si non trouvée.
        """
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if not model:
            return None  # Le pays n'existe pas

        # Mise à jour des champs
        model.name = payload.name
        model.iso2 = payload.iso2
        model.iso3 = payload.iso3
        model.code3 = payload.code3
        model.population = payload.population

        self.session.commit()
        return CountryMappingUtils.model_to_entity(model)

    def delete(self, id: int) -> Optional[CountryEntity]:
        """
        Supprime un pays de la base de données.

        Args:
            id (int): L'ID du pays à supprimer.

        Returns:
            Optional[CountryEntity]: L'entité supprimée ou None si non trouvée.
        """
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return CountryMappingUtils.model_to_entity(model)
        return None

    def find_by_id(self, id: int) -> Optional[CountryEntity]:
        """
        Recherche un pays par son ID.

        Args:
            id (int): L'ID du pays.

        Returns:
            Optional[CountryEntity]: L'entité trouvée ou None.
        """
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if model:
            return CountryMappingUtils.model_to_entity(model)
        return None
    
    def find_by_code3(self, code3: str) -> Optional[CountryEntity]:
        """
        Recherche un pays par son code3.

        Args:
            code3 (str): Le code3 du pays.

        Returns:
            Optional[CountryEntity]: L'entité trouvée ou None si non trouvée.
        """
        model = self.session.query(CountryModel).filter(CountryModel.code3 == code3).first()
        if model:
            return CountryMappingUtils.model_to_entity(model)
        return None
    
    def find_all(self) -> List[CountryEntity]:
        """
        Récupère tous les pays de la base de données.

        Returns:
            List[CountryEntity]: Liste des pays.
        """
        models = self.session.query(CountryModel).all()
        return [CountryMappingUtils.model_to_entity(model) for model in models]

    def exists(self, id: int) -> bool:
        """
        Vérifie si un pays existe dans la base de données.

        Args:
            id (int): L'ID du pays.

        Returns:
            bool: True si le pays existe, False sinon.
        """
        return self.session.query(CountryModel).filter(CountryModel.id == id).count() > 0