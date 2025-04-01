from typing import List

from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllVaccinesUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository):
        super().__init__(repository)

    def execute(self) -> List[VaccineEntity]:
        all_vaccines = self.repository.find_all()
        return all_vaccines