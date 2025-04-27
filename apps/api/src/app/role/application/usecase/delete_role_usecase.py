from fastapi import HTTPException, status
from src.app.role.domain.entity.role_entity import RoleEntity
from src.app.role.infrastructure.model.role_model import RoleModel
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class DeleteRoleUseCase(BaseUseCase):
    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    def execute(self, id: int) -> RoleModel | RoleEntity:
        try:
            role = self.repository.find_by_id(id)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Le rôle n'existe pas.",
                )
            return self.repository.delete(role)

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
