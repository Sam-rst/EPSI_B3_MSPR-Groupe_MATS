from typing import List

from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllCountriesUseCase(BaseUseCase):
    def __init__(self, repository: CountryRepository):
        super().__init__(repository)

    def execute(self) -> List[CountryEntity]:
        all_countries = self.repository.find_all()
        return all_countries