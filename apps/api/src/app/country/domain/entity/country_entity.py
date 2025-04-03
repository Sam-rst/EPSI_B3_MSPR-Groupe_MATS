from src.app.base.domain.entity.base_entity import BaseEntity


class CountryEntity(BaseEntity):

    def __init__(
        self,
        name: str,
        iso2: str,
        iso3: str,
        population: int,
    ):
        super().__init__()
        self._name = name
        self._iso2 = iso2
        self._iso3 = iso3
        self._population = population

    def print(self) -> str:
        return f"Country n°{self.id}: {self.name} ({self.iso2}, {self.iso3}) a {self.population} habitants"

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
    def iso2(self) -> str:
        return self._iso2

    @iso2.setter
    def iso2(self, value: str):
        if not value:
            raise ValueError("Le code ISO2 ne peut pas être vide.")
        self._iso2 = value
        self.update("system")

    @property
    def iso3(self) -> str:
        return self._iso3

    @iso3.setter
    def iso3(self, value: str):
        if not value:
            raise ValueError("Le code ISO3 ne peut pas être vide.")
        self._iso3 = value
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