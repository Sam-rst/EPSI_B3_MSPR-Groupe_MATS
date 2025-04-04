from datetime import datetime
from typing import List

from src.app.epidemic.presentation.model.payload.update_epidemic_payload import UpdateEpidemicPayload
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.epidemic.domain.entity.epidemic_entity import EpidemicEntity
from src.app.epidemic.presentation.model.payload.create_epidemic_payload import (
    CreateEpidemicPayload,
)

class EpidemicRepositoryInMemory(EpidemicRepository):
    def __init__(self):
        self._data: List[EpidemicEntity] = []

    def create(self, payload: CreateEpidemicPayload) -> EpidemicEntity:
        """Create a epidemic

        Args:
            entity (EpidemicEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        epidemic_created = EpidemicEntity(
            name=payload.name, iso2=payload.iso2, iso3=payload.iso3, population=payload.population
        )
        self._data.append(epidemic_created)
        return epidemic_created

    def update(self, entity: EpidemicEntity, payload: UpdateEpidemicPayload) -> EpidemicEntity:
        """Update the epidemic

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """        
        entity.name = payload.name
        entity.iso2 = payload.iso2
        entity.iso3 = payload.iso3
        entity.population = payload.population
        
        entity.update("system")
        return entity

    def delete(self, entity: EpidemicEntity) -> EpidemicEntity:
        """Delete the country

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        entity.delete("system")
        return entity
    
    def find_by_id(self, id: int) -> EpidemicEntity:
        """Find country by id

        Args:
            id (int): _description_

        Returns:
            CountryEntity: _description_
        """
        for epidemic in self._data:
            if epidemic.id == id:
                return epidemic
        return None


    def find_by_iso3(self, iso3: str) -> EpidemicEntity:
        """Find country by iso3

        Args:
            iso3 (str): _description_

        Returns:
            CountryEntity: _description_
        """
        for epidemic in self._data:
            if epidemic.iso3 == iso3:
                return epidemic
        return None
    
    def find_all(self) -> List[EpidemicEntity]:
        """Find all countries

        Returns:
            List[CountryEntity]: _description_
        """
        data = [epidemic for epidemic in self._data if not epidemic.is_deleted]
        return data
