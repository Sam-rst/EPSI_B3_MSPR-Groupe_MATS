from datetime import datetime
from typing import List, Optional

from src.app.vaccine.presentation.model.payload.update_vaccine_payload import UpdateVaccinePayload
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import CreateVaccinePayload


class VaccineRepositoryInMemory(VaccineRepository):
    def __init__(self):
        self._data: List[VaccineEntity] = []

    def create(self, payload: CreateVaccinePayload) -> VaccineEntity:
        """Create a vaccine

        Args:
            payload (CreateVaccinePayload): The payload for creating a vaccine.

        Returns:
            VaccineEntity: The created vaccine entity.
        """
        vaccine_created = VaccineEntity(
            name=payload.name,
            created_at=datetime.now(),
            created_by="system",
        )
        self._data.append(vaccine_created)
        return vaccine_created

    def update(self, entity: VaccineEntity, payload: UpdateVaccinePayload) -> VaccineEntity:
        """Update the vaccine

        Args:
            entity (VaccineEntity): The vaccine entity to update.
            payload (UpdateVaccinePayload): The payload containing updated data.

        Returns:
            VaccineEntity: The updated vaccine entity.
        """
        entity.name = payload.name
        entity.updated_at = datetime.now()
        entity.updated_by = "system"
        return entity

    def delete(self, entity: VaccineEntity) -> VaccineEntity:
        """Delete the vaccine

        Args:
            entity (VaccineEntity): The vaccine entity to delete.

        Returns:
            VaccineEntity: The logically deleted vaccine entity.
        """
        entity.delete("system")
        return entity

    def find_by_id(self, id: int) -> Optional[VaccineEntity]:
        """Find vaccine by ID

        Args:
            id (int): The ID of the vaccine.

        Returns:
            Optional[VaccineEntity]: The vaccine entity if found, otherwise None.
        """
        for vaccine in self._data:
            if vaccine.id == id:
                return vaccine
        return None

    def find_by_name(self, name: str) -> Optional[VaccineEntity]:
        """Find vaccine by name

        Args:
            name (str): The name of the vaccine.

        Returns:
            Optional[VaccineEntity]: The vaccine entity if found, otherwise None.
        """
        for vaccine in self._data:
            if vaccine.name == name:
                return vaccine
        return None

    def find_all(self) -> List[VaccineEntity]:
        """Find all vaccines

        Returns:
            List[VaccineEntity]: A list of all non-deleted vaccine entities.
        """
        return [vaccine for vaccine in self._data if not vaccine.is_deleted]

    def exists(self, id: int) -> bool:
        """Check if a vaccine exists by ID

        Args:
            id (int): The ID of the vaccine.

        Returns:
            bool: True if the vaccine exists, otherwise False.
        """
        for vaccine in self._data:
            if vaccine.id == id:
                return True
        return False