from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.user.presentation.model.payload.create_user_payload import CreateUserPayload
from src.app.user.presentation.model.payload.update_user_payload import UpdateUserPayload
from src.app.base.infrastructure.repository.base_repo_in_postgres import BaseRepositoryInPostgres


class UserRepositoryInPostgres(BaseRepositoryInPostgres):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        super().__init__(db.get_session())

    def create(self, payload: CreateUserPayload) -> UserModel:
        try:
            model = UserModel(
                firstname=payload.firstname,
                lastname=payload.lastname,
                username=payload.username,
                email=payload.email,
                password=payload.password,
                gender=payload.gender,
                birthdate=payload.birthdate,
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
            self.session.commit()

            return user
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
                self.session.query(UserModel)
                .filter(UserModel.email == email)
                .first()
            )

            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[UserModel]:
        """
        Récupère tous les utilisateurs non supprimés.

        Raises:
            e: Exception lors de la récupération des utilisateurs

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

    def reactivate(self, user: UserModel) -> UserModel:
        try:
            user.reactivate("system")
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e