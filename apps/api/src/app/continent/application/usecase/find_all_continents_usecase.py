from typing import List

from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllContinentsUseCase(BaseUseCase):
    def __init__(self, repository: ContinentRepository):
        super().__init__(repository)

    def execute(self) -> List[ContinentEntity]:
        all_continents = self.repository.find_all()
        not_deleted_continents = [continent for continent in all_continents if not continent.is_deleted]
        return not_deleted_continents