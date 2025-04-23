from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.auth.presentation.model.payload.register_payload import (
    RegisterPayload,
)
from src.app.user.presentation.model.payload.update_user_payload import (
    UpdateUserPayload,
)


class UserRepositoryInPostgres(UserRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: RegisterPayload) -> UserModel:
        try:
            email = f"{payload.username.lower()}@analyseit.com"
            firstname, lastname = payload.username.split(".", 1)
            firstname = firstname.capitalize()
            lastname = lastname.capitalize()

            # Créer le modèle utilisateur
            model = UserModel(
                firstname=firstname,
                lastname=lastname,
                username=payload.username,
                email=email,
                password=payload.password_hashed,
                country_id=payload.country_id,
                role_id=payload.role_id,
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, user: UserModel, payload: UpdateUserPayload
    ) -> Optional[UserModel]:
        try:
            pass
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, user: UserModel) -> Optional[UserModel]:
        try:
            user.delete("system")
            self.session.commit()

            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[UserModel]:
        try:
            user = self.session.query(UserModel).filter(UserModel.id == id).first()

            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_username(self, username: str) -> Optional[UserModel]:
        try:
            user = (
                self.session.query(UserModel)
                .filter(UserModel.username == username)
                .first()
            )

            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_email(self, email: str) -> Optional[UserModel]:
        try:
            user = (
                self.session.query(UserModel).filter(UserModel.email == email).first()
            )

            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[UserModel]:
        """
        Récupère tous les utilisateurs non supprimés.

        Returns:
            List[UserModel]: Liste des utilisateurs
        """
        try:
            users = (
                self.session.query(UserModel)
                .filter(UserModel.is_deleted == False)
                .all()
            )

            return users
        except Exception as e:
            self.session.rollback()
            raise e

    def verify_password(self, user: UserModel, password_to_verify: str) -> bool:
        try:
            return user.password == password_to_verify
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, user: UserModel) -> UserModel:
        try:
            user.reactivate("system")
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e
