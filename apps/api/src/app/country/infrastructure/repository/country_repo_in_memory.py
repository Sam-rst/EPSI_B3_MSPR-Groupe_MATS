from datetime import datetime
from typing import List

from src.app.country.presentation.model.payload.update_country_payload import UpdateCountryPayload
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)

class CountryRepositoryInMemory(CountryRepository):
    def __init__(self):
        self._data: List[CountryEntity] = []

    def create(self, payload: CreateCountryPayload) -> CountryEntity:
        """Create a country

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        country_created = CountryEntity(
            name=payload.name, iso2=payload.iso2, iso3=payload.iso3, population=payload.population
        )
        self._data.append(country_created)
        return country_created

    def update(self, entity: CountryEntity, payload: UpdateCountryPayload) -> CountryEntity:
        """Update the country

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

    def delete(self, entity: CountryEntity) -> CountryEntity:
        """Delete the country

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        entity.delete("system")
        return entity
    
    def find_by_id(self, id: int) -> CountryEntity:
        """Find country by id

        Args:
            id (int): _description_

        Returns:
            CountryEntity: _description_
        """
        for country in self._data:
            if country.id == id:
                return country
        return None


    def find_by_iso3(self, iso3: str) -> CountryEntity:
        """Find country by iso3

        Args:
            iso3 (str): _description_

        Returns:
            CountryEntity: _description_
        """
        for country in self._data:
            if country.iso3 == iso3:
                return country
        return None
    
    def find_all(self) -> List[CountryEntity]:
        """Find all countries

        Returns:
            List[CountryEntity]: _description_
        """
        data = [country for country in self._data if not country.is_deleted]
        return data
