from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.role.infrastructure.model.role_model import RoleModel
from src.app.role.presentation.model.payload.create_role_payload import (
    CreateRolePayload,
)
from src.app.role.presentation.model.payload.update_role_payload import (
    UpdateRolePayload,
)


class RoleRepositoryInPostgres(RoleRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateRolePayload) -> RoleModel:
        try:
            # Créer le modèle role
            model = RoleModel(
                name=payload.name,
                description=payload.description,
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, role: RoleModel, payload: UpdateRolePayload
    ) -> Optional[RoleModel]:
        try:
            if payload.name:
                role.name = payload.name
            if payload.description:
                role.description = payload.description

            role.update("system")
            self.session.commit()

            return role
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, role: RoleModel) -> Optional[RoleModel]:
        try:
            role.delete("system")
            self.session.commit()

            return role
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[RoleModel]:
        try:
            role = self.session.query(RoleModel).filter(RoleModel.id == id).first()

            return role
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_name(self, name: str) -> Optional[RoleModel]:
        try:
            role = self.session.query(RoleModel).filter(RoleModel.name == name).first()

            return role
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[RoleModel]:
        """
        Récupère tous les roles non supprimés.

        Returns:
            List[RoleModel]: Liste des roles
        """
        try:
            roles = (
                self.session.query(RoleModel)
                .filter(RoleModel.is_deleted == False)
                .all()
            )

            return roles
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, role: RoleModel) -> RoleModel:
        try:
            role.reactivate("system")
            self.session.commit()
            return role
        except Exception as e:
            self.session.rollback()
            raise e
