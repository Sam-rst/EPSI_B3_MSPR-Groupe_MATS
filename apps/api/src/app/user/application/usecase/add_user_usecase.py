from fastapi import HTTPException, status
from src.app.user.domain.entity.user_entity import UserEntity
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.user.presentation.model.payload.create_user_payload import CreateUserPayload
from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class AddUserUseCase(BaseUseCase):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def execute(self, payload: CreateUserPayload) -> UserModel:
        try:
            # Déduire le firstname et le lastname à partir du username
            if "." not in payload.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le username doit être au format 'firstname.lastname'.",
                )

            # Générer l'email
            email = f"{payload.username.lower()}@analyseit.com"

            # Vérifier si un utilisateur avec cet email existe déjà
            existing_user = self.repository.find_by_email(email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Un utilisateur avec cet email existe déjà.",
                )

            # Sauvegarder l'utilisateur dans le repository
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