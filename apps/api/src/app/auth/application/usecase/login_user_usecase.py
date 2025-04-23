from fastapi import HTTPException, status

from src.app.user.domain.interface.user_repository import UserRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.auth.presentation.model.payload.login_payload import LoginPayload
from src.app.auth.presentation.model.response.login_response import LoginResponse
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.auth.infrastructure.service.jwt_service import JWTService


class LoginUserUseCase(BaseUseCase):
    def __init__(
        self,
        user_repository: UserRepository,
        country_repository: CountryRepository,
        role_repository: RoleRepository,
        jwt_service: JWTService,
    ):
        self._user_repository = user_repository
        self._country_repository = country_repository
        self._role_repository = role_repository
        self._jwt_service = jwt_service

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    @property
    def country_repository(self) -> CountryRepository:
        return self._country_repository

    @property
    def role_repository(self) -> RoleRepository:
        return self._role_repository

    @property
    def jwt_service(self) -> JWTService:
        return self._jwt_service

    def execute(self, payload: LoginPayload) -> LoginResponse:
        try:
            # Déduire le firstname et le lastname à partir du username
            if "." not in payload.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le username doit être au format 'firstname.lastname'.",
                )

            # Vérifier si un utilisateur avec ce username existe déjà
            user = self.user_repository.find_by_username(payload.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Le username n'existe pas.",
                )

            # Vérifier si le mot de passe est correct
            if not self.user_repository.verify_password(user, payload.password_hashed):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Mot de passe incorrect.",
                )

            return LoginResponse(
                id=user.id,
                firstname=user.firstname,
                lastname=user.lastname,
                username=user.username,
                email=user.email,
                role_id=user.role_id,
                country_id=user.country_id,
                access_token=self.jwt_service.create_access_token(
                    data={"sub": user.username, "id": user.id}
                ),
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
