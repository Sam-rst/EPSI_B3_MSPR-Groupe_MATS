from fastapi import HTTPException, status
from typing import List
from src.app.role.domain.entity.role_entity import RoleEntity
from src.app.role.infrastructure.model.role_model import RoleModel
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllRolesUseCase(BaseUseCase):
    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    def execute(self) -> List[RoleEntity] | List[RoleModel]:
        try:
            roles = self.repository.find_all()
            return roles

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue: {str(e)}",
            )
