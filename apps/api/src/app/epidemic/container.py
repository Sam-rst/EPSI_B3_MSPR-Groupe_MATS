from dependency_injector import containers, providers

from src.config.config import Config

from src.app.epidemic.infrastructure.repository.epidemic_repo_in_memory import (
    EpidemicRepositoryInMemory,
)
from src.app.epidemic.infrastructure.repository.epidemic_repo_in_postgres import (
    EpidemicRepositoryInPostgres,
)
from src.app.epidemic.application.usecase.add_epidemic_usecase import (
    AddEpidemicUseCase,
)
from src.app.epidemic.application.usecase.find_all_epidemics_usecase import (
    FindAllEpidemicsUseCase,
)
from src.app.epidemic.application.usecase.find_epidemic_by_id_usecase import (
    FindEpidemicByIdUseCase,
)
from src.app.epidemic.application.usecase.update_epidemic_usecase import (
    UpdateEpidemicUseCase,
)
from src.app.epidemic.application.usecase.delete_epidemic_usecase import (
    DeleteEpidemicUseCase,
)
from src.app.epidemic.application.usecase.import_epidemics_usecase import (
    ImportEpidemicsUseCase,
)


class EpidemicContainer(containers.DeclarativeContainer):
    modules = ["src.app.epidemic.presentation.router"]
    config = providers.Singleton(Config)

    # Définir les repositories
    repository_in_memory = providers.Singleton(EpidemicRepositoryInMemory)
    repository_in_postgres = providers.Singleton(EpidemicRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        config.provided.REPOSITORY_TYPE,
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    add_epidemic_usecase = providers.Factory(AddEpidemicUseCase, repository=repository)
    find_all_epidemics_usecase = providers.Factory(
        FindAllEpidemicsUseCase, repository=repository
    )
    find_epidemic_by_id_usecase = providers.Factory(
        FindEpidemicByIdUseCase, repository=repository
    )
    update_epidemic_usecase = providers.Factory(
        UpdateEpidemicUseCase,
        repository=repository,
    )
    delete_epidemic_usecase = providers.Factory(
        DeleteEpidemicUseCase, repository=repository
    )
    import_epidemics_usecase = providers.Factory(
        ImportEpidemicsUseCase, repository=repository
    )
