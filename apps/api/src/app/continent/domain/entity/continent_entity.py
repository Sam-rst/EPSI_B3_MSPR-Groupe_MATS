from src.app.base.domain.entity.base_entity import BaseEntity


class ContinentEntity(BaseEntity):

    def __init__(
        self,
        name: str,
        code: str,
        population: int,
        created_by: str | None = None,
        updated_by: str | None = None,
    ):
        super().__init__(created_by, updated_by)
        self._name = name
        self._code = code
        self._population = population

    def __str__(self) -> str:
        return self.print()

    def print(self) -> str:
        return f"Continent n°{self.id}: {self.name} ({self.code}) a {self.population} habitants"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Le nom ne peut pas être vide.")
        self._name = value
        self.update("system")

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str):
        if not value:
            raise ValueError("Le code ne peut pas être vide.")
        self._code = value
        self.update("system")

    @property
    def population(self) -> int:
        return self._population

    @population.setter
    def population(self, value: int):
        if value < 0:
            raise ValueError("La population ne peut pas être négative.")
        elif value == 0:
            raise ValueError("La population ne peut pas être nulle.")
        self._population = value
        self.update("system")

    def update(self, updated_by: str):
        return super().update(updated_by)

    def delete(self, deleted_by: str):
        return super().delete(deleted_by)
