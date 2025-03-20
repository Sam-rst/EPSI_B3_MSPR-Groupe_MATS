from datetime import datetime
from typing import List

from src.app.continent.presentation.model.payload.update_continent_payload import UpdateContinentPayload
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.utils.continent_mapping_utils import ContinentMappingUtils
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)

class ContinentRepositoryInMemory(ContinentRepository):
    def __init__(self):
        self._data: List[ContinentEntity] = []

    def create(self, payload: CreateContinentPayload) -> ContinentEntity:
        """Create a continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        continent_created = ContinentEntity(
            name=payload.name, code=payload.code, population=payload.population
        )
        self.data.append(continent_created)
        return continent_created

    def update(self, entity: ContinentEntity, payload: UpdateContinentPayload) -> ContinentEntity:
        """Update the continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """        
        entity.name = payload.name
        entity.code = payload.code
        entity.population = payload.population
        
        entity.update("system")
        return entity

    def delete(self, entity: ContinentEntity) -> ContinentEntity:
        """Delete the continent

        Args:
            entity (ContinentEntity): _description_

        Returns:
            ContinentEntity: _description_
        """
        entity.delete("system")
        return entity
    
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
        return None


    def find_by_code(self, code: str) -> ContinentEntity:
        """Find continent by code

        Args:
            code (str): _description_

        Returns:
            ContinentEntity: _description_
        """
        for continent in self.data:
            if continent.code == code:
                return continent
        return None
    
    def find_all(self) -> List[ContinentEntity]:
        """Find all continents

        Returns:
            List[ContinentEntity]: _description_
        """
        data = [continent for continent in self.data if not continent.is_deleted]
        return data

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
