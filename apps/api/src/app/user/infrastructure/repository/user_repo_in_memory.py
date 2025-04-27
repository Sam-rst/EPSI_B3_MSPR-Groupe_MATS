from typing import List, Optional
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.auth.presentation.model.payload.register_payload import RegisterPayload
from src.app.user.presentation.model.payload.update_user_payload import UpdateUserPayload


class UserRepositoryInMemory(UserRepository):
    def __init__(self):
        self._data: List[UserEntity] = []

    def create(self, payload: RegisterPayload) -> UserEntity:
        """Crée un utilisateur en mémoire."""
        user_created = UserEntity(
            firstname=payload.firstname,
            lastname=payload.lastname,
            username=payload.username,
            email=payload.email,
            password=payload.password_has,
        )
        self._data.append(user_created)
        return user_created

    def update(self, user: UserEntity, payload: UpdateUserPayload) -> UserEntity:
        """Met à jour un utilisateur en mémoire."""
        if payload.firstname:
            user.firstname = payload.firstname
        if payload.lastname:
            user.lastname = payload.lastname
        if payload.username:
            user.username = payload.username
        if payload.email:
            user.email = payload.email
        if payload.password:
            user.password = payload.password
        if payload.gender:
            user.gender = payload.gender
        if payload.birthdate:
            user.birthdate = payload.birthdate
        if payload.roles:
            user.roles = payload.roles

        user.update("system")
        return user

    def delete(self, user: UserEntity) -> UserEntity:
        """Supprime un utilisateur en mémoire."""
        user.delete("system")
        return user

    def find_by_id(self, id: int) -> Optional[UserEntity]:
        """Recherche un utilisateur par son ID."""
        for user in self._data:
            if user.id == id:
                return user
        return None

    def find_by_username(self, username: str) -> Optional[UserEntity]:
        """Recherche un utilisateur par son nom d'utilisateur."""
        for user in self._data:
            if user.username == username:
                return user
        return None

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        """Recherche un utilisateur par son email."""
        for user in self._data:
            if user.email == email:
                return user
        return None

    def find_all(self) -> List[UserEntity]:
        """Récupère tous les utilisateurs non supprimés."""
        return [user for user in self._data if not user.is_deleted]
    
    def verify_password(
        self, user: UserEntity, password_to_verify: str
    ) -> bool:
        """Vérifie le mot de passe d'un utilisateur."""
        return user.verify_password(password_to_verify)

    def reactivate(self, user: UserEntity) -> UserEntity:
        """Réactive un utilisateur supprimé."""
        user.reactivate("system")
        return user