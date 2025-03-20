from datetime import datetime
from typing import Optional


class BaseEntity:
    _id_counter = 0

    def __init__(
        self
    ):
        BaseEntity._id_counter += 1

        self._id = BaseEntity._id_counter
        self._created_at: datetime = datetime.now()
        self._created_by: str = "system"
        self._updated_at: datetime = datetime.now()
        self._updated_by: str = "system"
        self._deleted_at: Optional[datetime] = None
        self._deleted_by: Optional[str] = None
        self._is_deleted: bool = False

    def __str__(self) -> str:
        return self.print()

    def print(self) -> str:
        return ""

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime):
        self._created_at = value

    @property
    def created_by(self) -> Optional[str]:
        return self._created_by

    @created_by.setter
    def created_by(self, value: str):
        if not value:
            raise ValueError("Le nom du créateur ne peut pas être vide.")
        self._updated_by = value

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: datetime):
        self._updated_at = value

    @property
    def updated_by(self) -> Optional[str]:
        return self._updated_by

    @updated_by.setter
    def updated_by(self, value: str):
        if not value:
            raise ValueError("Le nom du modifieur ne peut pas être vide.")
        self._updated_by = value

    @property
    def deleted_at(self) -> Optional[datetime]:
        return self._deleted_at

    @deleted_at.setter
    def deleted_at(self, value: datetime):
        self._deleted_at = value

    @property
    def deleted_by(self) -> Optional[str]:
        return self._deleted_by

    @deleted_by.setter
    def deleted_by(self, value: str):
        if not value:
            raise ValueError("Le nom du supprimeur ne peut pas être vide.")
        self._deleted_by = value

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, value: bool):
        self._is_deleted = value

    def update(self, updated_by: str):
        self.updated_at = datetime.now()
        self.updated_by = updated_by

    def delete(self, deleted_by: str):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.deleted_by = deleted_by
        self.update(deleted_by)
