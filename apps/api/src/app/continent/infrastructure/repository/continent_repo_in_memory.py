from typing import List

from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity


class ContinentRepositoryInMemory(ContinentRepository):
    def __init__(self):
        self._data: List[ContinentEntity] = []

    @property
    def data(self) -> List[ContinentEntity]:
        return self._data

    @data.setter
    def data(self, value: List[ContinentEntity]):
        self._data = value

    def create(self, entity: ContinentEntity) -> ContinentEntity:
        """Create a continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        self._data.append(entity)
        return entity

    def update(self, entity: ContinentEntity) -> ContinentEntity:
        """Update the continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        for index, continent in enumerate(self.data):
            if continent.id == entity.id:
                entityToUpdate = self.data[index]
                entityToUpdate.update("system")
                self.data[index] = entityToUpdate
                return entityToUpdate

        raise ValueError("Le continent n'a pas été trouvé")


    def delete(self, entity: ContinentEntity) -> ContinentEntity:
        """Delete the entity

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        for index, continent in enumerate(self.data):
            if continent.id == entity.id:
                entityToUpdate = self.data[index]
                entityToUpdate.update("system")
                self.data[index] = entityToUpdate
                return entityToUpdate

        raise ValueError("Le continent n'a pas été trouvé")

    def find_by_id(self, id: int) -> ContinentEntity:
        """Find continent by id

        Args:
            id (int): _description_

        Returns:
            ContinentEntity: _description_
        """
        for continent in self.data:
            if continent.id == id:
                return continent

        raise ValueError("Le continent n'a pas été trouvé")

    def find_all(self) -> List[ContinentEntity]:
        """Find all continents

        Returns:
            List[ContinentEntity]: _description_
        """
        return self.data

    def exists(self, id: int) -> bool:
        """Search if continent exists

        Args:
            id (int): _description_

        Returns:
            bool: _description_
        """
        for continent in self.data:
            if continent.id == id:
                return True

        return False
