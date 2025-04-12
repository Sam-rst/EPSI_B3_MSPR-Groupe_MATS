from dependency_injector import containers, providers

from src.config.config import Config

from src.app.continent.infrastructure.repository.continent_repo_in_memory import (
    ContinentRepositoryInMemory,
)
from src.app.continent.infrastructure.repository.continent_repo_in_postgres import (
    ContinentRepositoryInPostgres,
)
from src.app.continent.application.usecase.add_continent_usecase import (
    AddContinentUseCase,
)
from src.app.continent.application.usecase.find_all_continents_usecase import (
    FindAllContinentsUseCase,
)
from src.app.continent.application.usecase.find_continent_by_id_usecase import (
    FindContinentByIdUseCase,
)
from src.app.continent.application.usecase.update_continent_usecase import (
    UpdateContinentUseCase,
)
from src.app.continent.application.usecase.delete_continent_usecase import (
    DeleteContinentUseCase,
)
from src.app.continent.application.usecase.import_continents_usecase import (
    ImportContinentsUseCase,
)


class ContinentContainer(containers.DeclarativeContainer):
    modules = ["src.app.continent.presentation.router"]
    config = providers.Singleton(Config)

    # Définir les repositories
    repository_in_memory = providers.Singleton(ContinentRepositoryInMemory)
    repository_in_postgres = providers.Singleton(ContinentRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        config.provided.REPOSITORY_TYPE,
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    add_continent_usecase = providers.Factory(
        AddContinentUseCase, repository=repository
    )
    find_all_continents_usecase = providers.Factory(
        FindAllContinentsUseCase, repository=repository
    )
    find_continent_by_id_usecase = providers.Factory(
        FindContinentByIdUseCase, repository=repository
    )
    update_continent_usecase = providers.Factory(
        UpdateContinentUseCase, repository=repository
    )
    delete_continent_usecase = providers.Factory(
        DeleteContinentUseCase, repository=repository
    )
    import_continents_usecase = providers.Factory(
        ImportContinentsUseCase, repository=repository
    )
