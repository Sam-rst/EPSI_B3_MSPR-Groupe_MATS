from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)


class VaccineRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create(self, payload: CreateVaccinePayload) -> VaccineEntity | VaccineModel:
        pass

    @abstractmethod
    def update(self, payload: UpdateVaccinePayload) -> VaccineEntity | VaccineModel:
        pass

    @abstractmethod
    def delete(self, id: int) -> VaccineEntity | VaccineModel:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> VaccineEntity | VaccineModel:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> VaccineEntity | VaccineModel:
        pass

    @abstractmethod
    def find_all(self) -> List[VaccineEntity]:
        pass

    @abstractmethod
    def reactivate(
        self, vaccine: VaccineEntity | VaccineModel
    ) -> VaccineEntity | VaccineModel:
        pass