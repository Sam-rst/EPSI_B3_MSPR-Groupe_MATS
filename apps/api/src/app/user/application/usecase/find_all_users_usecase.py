from fastapi import HTTPException, status
from typing import List
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindAllUsersUseCase(BaseUseCase):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def execute(self) -> List[UserEntity] | List[UserModel]:
        try:
            users = self.repository.find_all()
            return users

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue: {str(e)}",
            )