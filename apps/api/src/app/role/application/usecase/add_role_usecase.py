from fastapi import HTTPException, status
from src.app.role.domain.entity.role_entity import RoleEntity
from src.app.role.infrastructure.model.role_model import RoleModel
from src.app.role.presentation.model.payload.create_role_payload import (
    CreateRolePayload,
)
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddRoleUseCase(BaseUseCase):
    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    def execute(self, payload: CreateRolePayload) -> RoleModel | RoleEntity:
        try:
            existing_role = self.repository.find_by_name(payload.name)
            if existing_role:
                if not existing_role.is_deleted:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le nom du role existe déjà",
                    )
                else:
                    # Si le role existe mais est supprimé, on le restaure
                    self.repository.reactivate(existing_role)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Le role existe déjà, il a été supprimé mais il vient d'être restauré.",
                    )
            return self.repository.create(payload)

        except HTTPException as http_exc:
            raise HTTPException(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue: {str(e)}",
            )
