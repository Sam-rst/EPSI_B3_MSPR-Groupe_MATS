from typing import List
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.country.domain.entity.country_entity import CountryEntity


class CountryRepositoryInPostgres(CountryRepository):
    def __init__(self):
        self._data = []

    def create(self, entity: CountryEntity) -> CountryEntity:
        """Create a country

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        pass

    def update(self, entity: CountryEntity) -> CountryEntity:
        """Update the country

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        pass

    def delete(self, entity: CountryEntity) -> CountryEntity:
        """Delete the entity

        Args:
            entity (CountryEntity): _description_

        Returns:
            CountryEntity: _description_
        """
        pass

    def find_by_id(self, id: int) -> CountryEntity:
        """Find country by id

        Args:
            id (int): _description_

        Returns:
            CountryEntity: _description_
        """
        pass

    def find_all(self) -> List[CountryEntity]:
        """Find all countrys

        Returns:
            List[CountryEntity]: _description_
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