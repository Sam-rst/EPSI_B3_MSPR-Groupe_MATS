from dependency_injector import containers, providers

from src.core.config import settings

from src.app.user.infrastructure.repository.user_repo_in_memory import (
    UserRepositoryInMemory,
)
from src.app.user.infrastructure.repository.user_repo_in_postgres import (
    UserRepositoryInPostgres,
)
from src.app.auth.application.usecase.register_user_usecase import RegisterUserUseCase
from src.app.auth.application.usecase.login_user_usecase import LoginUserUseCase
from src.app.auth.application.usecase.change_password_usecase import (
    ChangePasswordUseCase,
)
from src.app.auth.infrastructure.service.jwt_service import JWTService


class AuthContainer(containers.DeclarativeContainer):
    modules = ["src.app.auth.presentation.router"]
    

    # Définir les repositories
    repository_user_in_memory = providers.Singleton(UserRepositoryInMemory)
    repository_user_in_postgres = providers.Singleton(UserRepositoryInPostgres)

    repository_country_in_memory = providers.Singleton(UserRepositoryInMemory)
    repository_country_in_postgres = providers.Singleton(UserRepositoryInPostgres)

    repository_role_in_memory = providers.Singleton(UserRepositoryInMemory)
    repository_role_in_postgres = providers.Singleton(UserRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    user_repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_user_in_memory,
        in_postgres=repository_user_in_postgres,
    )

    country_repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_country_in_memory,
        in_postgres=repository_country_in_postgres,
    )

    role_repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_role_in_memory,
        in_postgres=repository_role_in_postgres,
    )

    # Services
    jwt_service = providers.Singleton(JWTService)

    # Définir les usecases
    register_user_usecase = providers.Factory(
        RegisterUserUseCase, user_repository=user_repository
    )
    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        user_repository=user_repository,
        country_repository=country_repository,
        role_repository=role_repository,
        jwt_service=jwt_service,
    )
    change_password_usecase = providers.Factory(
        ChangePasswordUseCase, user_repository=user_repository
    )
