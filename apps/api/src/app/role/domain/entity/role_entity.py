from src.app.base.domain.entity.base_entity import BaseEntity


class RoleEntity(BaseEntity):
    def __init__(
        self,
        name: str,
        description: str = None,
    ):
        super().__init__()
        self._name = name
        self._description = description

    def print(self) -> str:
        return f"Rôle n°{self.id}: {self.name} --> {self.description}"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    def update(self, updated_by: str):
        return super().update(updated_by)

    def delete(self, deleted_by: str):
        return super().delete(deleted_by)
