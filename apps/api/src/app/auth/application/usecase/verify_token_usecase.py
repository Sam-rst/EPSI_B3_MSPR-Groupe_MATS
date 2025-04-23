from fastapi import HTTPException, status

from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.auth.presentation.model.response.login_response import LoginResponse
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.auth.infrastructure.service.jwt_service import JWTService


class VerifyTokenUseCase(BaseUseCase):
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
    ):
        self._user_repository = user_repository
        self._jwt_service = jwt_service

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    @property
    def jwt_service(self) -> JWTService:
        return self._jwt_service

    def execute(self, token: str) -> dict:
        try:
            # Vérifier si le token est valide
            payload = self.jwt_service.verify_token(token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide.",
                )

            return payload

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
