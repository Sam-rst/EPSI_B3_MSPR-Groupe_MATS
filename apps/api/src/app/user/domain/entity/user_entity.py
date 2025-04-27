from src.app.base.domain.entity.base_entity import BaseEntity


class UserEntity(BaseEntity):
    def __init__(
        self,
        firstname: str,
        lastname: str,
        username: str,
        email: str,
        password: str,
        gender: str = None,
        birthdate: str = None,
    ):
        super().__init__()
        self._firstname = firstname
        self._lastname = lastname
        self._username = username
        self._email = email
        self._password = password
        self._gender = gender
        self._birthdate = birthdate
        self._roles = []

    def print(self) -> str:
        return f"Utilisateur n°{self.id}: {self.firstname} {self.lastname} ({self.username}, {self.email})"

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, value: str):
        if not value:
            raise ValueError("Le prénom ne peut pas être vide.")
        self._firstname = value
        self.update("system")

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, value: str):
        if not value:
            raise ValueError("Le nom ne peut pas être vide.")
        self._lastname = value
        self.update("system")

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        if not value:
            raise ValueError("Le nom d'utilisateur ne peut pas être vide.")
        self._username = value
        self.update("system")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value:
            raise ValueError("L'email ne peut pas être vide.")
        self._email = value
        self.update("system")

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        if not value:
            raise ValueError("Le mot de passe ne peut pas être vide.")
        self._password = value
        self.update("system")

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str):
        self._gender = value
        self.update("system")

    @property
    def birthdate(self) -> str:
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value: str):
        self._birthdate = value
        self.update("system")

    @property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, value):
        self._roles = value
        self.update("system")

    def verify_password(self, password_to_verify: str) -> bool:
        """Vérifie le mot de passe de l'utilisateur."""
        return self._password == password_to_verify

    def update(self, updated_by: str):
        return super().update(updated_by)

    def delete(self, deleted_by: str):
        return super().delete(deleted_by)
