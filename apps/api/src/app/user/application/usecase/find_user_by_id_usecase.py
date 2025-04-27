from fastapi import HTTPException, status
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindUserByIdUseCase(BaseUseCase):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def execute(self, id: int) -> UserEntity | UserModel:
        try:
            user = self.repository.find_by_id(id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="L'utilisateur n'existe pas.",
                )
            return user

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