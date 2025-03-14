from typing import List

from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity


class ContinentRepositoryInPostgres(ContinentRepository):
    def __init__(self):
        self._data = []

    def create(self, entity: ContinentEntity) -> ContinentEntity:
        """Create a continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        pass

    def update(self, entity: ContinentEntity) -> ContinentEntity:
        """Update the continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        pass

    def delete(self, entity: ContinentEntity) -> ContinentEntity:
        """Delete the entity

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        pass

    def find_by_id(self, id: int) -> ContinentEntity:
        """Find continent by id

        Args:
            id (int): _description_

        Returns:
            ContinentEntity: _description_
        """
        pass

    def find_all(self) -> List[ContinentEntity]:
        """Find all continents

        Returns:
            List[ContinentEntity]: _description_
        """
        pass

    def exists(self, id: int) -> bool:
        """Search if entity exists

        Args:
            id (int): _description_

        Returns:
            bool: _description_
        """
        pass
