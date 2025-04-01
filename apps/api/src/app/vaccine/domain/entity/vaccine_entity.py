from src.app.base.domain.entity.base_entity import BaseEntity


class VaccineEntity(BaseEntity):
    def __init__(
        self,
        name: str
    ):
        super().__init__()
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Le nom du vaccin ne peut pas être vide.")
        self._name = value
        self.update("system")

    def update(self, updated_by: str):
        """
        Met à jour les informations de l'entité.

        Args:
            updated_by (str): L'utilisateur ayant effectué la mise à jour.
        """
        return super().update(updated_by)

    def delete(self, deleted_by: str):
        """
        Supprime logiquement l'entité.

        Args:
            deleted_by (str): L'utilisateur ayant effectué la suppression.
        """
        return super().delete(deleted_by)

    def __repr__(self) -> str:
        """
        Retourne une représentation lisible de l'entité Vaccine.

        Returns:
            str: Représentation de l'entité.
        """
        return (
            f"VaccineEntity(id={self.id}, name='{self.name}', "
            f"created_at={self.created_at}, created_by='{self.created_by}', "
            f"updated_at={self.updated_at}, updated_by='{self.updated_by}')"
        )