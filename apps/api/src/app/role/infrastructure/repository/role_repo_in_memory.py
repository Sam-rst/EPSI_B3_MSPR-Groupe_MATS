from typing import List, Optional
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.role.domain.entity.role_entity import RoleEntity
from src.app.role.presentation.model.payload.create_role_payload import (
    CreateRolePayload,
)
from src.app.role.presentation.model.payload.update_role_payload import (
    UpdateRolePayload,
)


class RoleRepositoryInMemory(RoleRepository):
    def __init__(self):
        self._data: List[RoleEntity] = []

    def create(self, payload: CreateRolePayload) -> RoleEntity:
        """Crée un role en mémoire."""
        role_created = RoleEntity(
            name=payload.name,
            description=payload.description,
        )
        self._data.append(role_created)
        return role_created

    def update(self, role: RoleEntity, payload: UpdateRolePayload) -> RoleEntity:
        """Met à jour un utilisateur en mémoire."""
        if payload.name:
            role.name = payload.name
        if payload.description:
            role.description = payload.description

        role.update("system")
        return role

    def delete(self, role: RoleEntity) -> RoleEntity:
        """Supprime un role en mémoire."""
        role.delete("system")
        return role

    def find_by_id(self, id: int) -> Optional[RoleEntity]:
        """Recherche un role par son ID."""
        for role in self._data:
            if role.id == id:
                return role
        return None

    def find_by_name(self, name: str) -> Optional[RoleEntity]:
        """Recherche un role par son nom."""
        for role in self._data:
            if role.name == name:
                return role
        return None

    def find_all(self) -> List[RoleEntity]:
        """Récupère tous les roles non supprimés."""
        return [role for role in self._data if not role.is_deleted]

    def reactivate(self, role: RoleEntity) -> RoleEntity:
        """Réactive un role supprimé."""
        role.reactivate("system")
        return role
