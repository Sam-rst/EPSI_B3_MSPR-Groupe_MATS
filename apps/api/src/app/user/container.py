from dependency_injector import containers, providers

from src.core.config import settings

from src.app.user.infrastructure.repository.user_repo_in_memory import (
    UserRepositoryInMemory,
)
from src.app.user.infrastructure.repository.user_repo_in_postgres import (
    UserRepositoryInPostgres,
)
from src.app.user.application.usecase.add_user_usecase import AddUserUseCase
from src.app.user.application.usecase.find_all_users_usecase import FindAllUsersUseCase
from src.app.user.application.usecase.find_user_by_id_usecase import (
    FindUserByIdUseCase,
)
from src.app.user.application.usecase.find_user_by_username_usecase import (
    FindUserByUsernameUseCase,
)
from src.app.user.application.usecase.update_user_usecase import UpdateUserUseCase
from src.app.user.application.usecase.delete_user_usecase import DeleteUserUseCase


class UserContainer(containers.DeclarativeContainer):
    modules = ["src.app.user.presentation.router"]

    # Définir les repositories
    repository_in_memory = providers.Singleton(UserRepositoryInMemory)
    repository_in_postgres = providers.Singleton(UserRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    add_user_usecase = providers.Factory(AddUserUseCase, repository=repository)
    find_all_users_usecase = providers.Factory(
        FindAllUsersUseCase, repository=repository
    )
    find_user_by_id_usecase = providers.Factory(
        FindUserByIdUseCase, repository=repository
    )
    find_user_by_username_usecase = providers.Factory(
        FindUserByUsernameUseCase, repository=repository
    )
    update_user_usecase = providers.Factory(
        UpdateUserUseCase,
        repository=repository,
    )
    delete_user_usecase = providers.Factory(DeleteUserUseCase, repository=repository)
