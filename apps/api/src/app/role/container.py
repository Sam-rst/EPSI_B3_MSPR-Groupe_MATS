from dependency_injector import containers, providers

from src.core.config import settings

from src.app.role.infrastructure.repository.role_repo_in_memory import (
    RoleRepositoryInMemory,
)
from src.app.role.infrastructure.repository.role_repo_in_postgres import (
    RoleRepositoryInPostgres,
)
from src.app.role.application.usecase.add_role_usecase import AddRoleUseCase
from src.app.role.application.usecase.find_all_roles_usecase import FindAllRolesUseCase
from src.app.role.application.usecase.find_role_by_id_usecase import (
    FindRoleByIdUseCase,
)
from src.app.role.application.usecase.update_role_usecase import UpdateRoleUseCase
from src.app.role.application.usecase.delete_role_usecase import DeleteRoleUseCase
from src.app.role.application.usecase.import_roles_usecase import (
    ImportRolesUseCase,
)


class RoleContainer(containers.DeclarativeContainer):
    modules = ["src.app.role.presentation.router"]

    # Définir les repositories
    repository_in_memory = providers.Singleton(RoleRepositoryInMemory)
    repository_in_postgres = providers.Singleton(RoleRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    add_role_usecase = providers.Factory(AddRoleUseCase, repository=repository)
    find_all_roles_usecase = providers.Factory(
        FindAllRolesUseCase, repository=repository
    )
    find_role_by_id_usecase = providers.Factory(
        FindRoleByIdUseCase, repository=repository
    )
    update_role_usecase = providers.Factory(
        UpdateRoleUseCase,
        repository=repository,
    )
    delete_role_usecase = providers.Factory(DeleteRoleUseCase, repository=repository)
    import_roles_usecase = providers.Factory(ImportRolesUseCase, repository=repository)
