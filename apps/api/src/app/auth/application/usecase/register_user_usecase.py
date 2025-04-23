from fastapi import HTTPException, status
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.user.presentation.model.payload.create_user_payload import (
    CreateUserPayload,
)
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.auth.presentation.model.payload.register_payload import RegisterPayload
from src.app.auth.presentation.model.response.register_response import RegisterResponse


class RegisterUserUseCase(BaseUseCase):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    def execute(self, payload: RegisterPayload) -> RegisterResponse:
        try:
            # Déduire le firstname et le lastname à partir du username
            if "." not in payload.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le username doit être au format 'firstname.lastname'.",
                )

            # Vérifier si un utilisateur avec ce username existe déjà
            existing_user = self.user_repository.find_by_username(payload.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Un utilisateur avec ce username existe déjà, veuillez en choisir un autre.",
                )

            # Sauvegarder l'utilisateur dans le repository user
            user = self.user_repository.create(payload)
            return RegisterResponse(
                id=user.id,
                firstname=user.firstname,
                lastname=user.lastname,
                username=user.username,
                email=user.email,
                role_id=user.role_id,
                country_id=user.country_id,
            )

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
