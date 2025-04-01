from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import CreateVaccinePayload


class VaccineRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create(self, payload: CreateVaccinePayload) -> VaccineEntity:
        """
        Crée un vaccin dans la base de données.

        Args:
            payload (CreateVaccinePayload): Les données pour créer un vaccin.

        Returns:
            VaccineEntity: L'entité créée.
        """
        pass

    @abstractmethod
    def update(self, payload) -> VaccineEntity:
        """
        Met à jour un vaccin dans la base de données.

        Args:
            payload: Les données pour mettre à jour un vaccin.

        Returns:
            VaccineEntity: L'entité mise à jour.
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> VaccineEntity:
        """
        Supprime un vaccin de la base de données.

        Args:
            id (int): L'ID du vaccin à supprimer.

        Returns:
            VaccineEntity: L'entité supprimée.
        """
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> VaccineEntity:
        """
        Recherche un vaccin par son ID.

        Args:
            id (int): L'ID du vaccin.

        Returns:
            VaccineEntity: L'entité trouvée.
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> VaccineEntity:
        """
        Recherche un vaccin par son nom.

        Args:
            name (str): Le nom du vaccin.

        Returns:
            VaccineEntity: L'entité trouvée.
        """
        pass

    @abstractmethod
    def find_all(self) -> List[VaccineEntity]:
        """
        Récupère tous les vaccins de la base de données.

        Returns:
            List[VaccineEntity]: Liste des entités trouvées.
        """
        pass

    @abstractmethod
    def exists(self, id: int) -> bool:
        """
        Vérifie si un vaccin existe dans la base de données.

        Args:
            id (int): L'ID du vaccin.

        Returns:
            bool: True si le vaccin existe, False sinon.
        """
        pass