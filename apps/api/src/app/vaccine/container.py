from dependency_injector import containers, providers

from src.config.config import Config

from src.app.vaccine.infrastructure.repository.vaccine_repo_in_memory import (
    VaccineRepositoryInMemory,
)
from src.app.vaccine.infrastructure.repository.vaccine_repo_in_postgres import (
    VaccineRepositoryInPostgres,
)
from src.app.vaccine.application.usecase.add_vaccine_usecase import (
    AddVaccineUseCase,
)
from src.app.vaccine.application.usecase.find_all_vaccines_usecase import (
    FindAllVaccinesUseCase,
)
from src.app.vaccine.application.usecase.find_vaccine_by_id_usecase import (
    FindVaccineByIdUseCase,
)
from src.app.vaccine.application.usecase.update_vaccine_usecase import (
    UpdateVaccineUseCase,
)
from src.app.vaccine.application.usecase.delete_vaccine_usecase import (
    DeleteVaccineUseCase,
)
from src.app.epidemic.infrastructure.repository.epidemic_repo_in_memory import (
    EpidemicRepositoryInMemory,
)
from src.app.epidemic.infrastructure.repository.epidemic_repo_in_postgres import (
    EpidemicRepositoryInPostgres,
)


class VaccineContainer(containers.DeclarativeContainer):
    modules = ["src.app.vaccine.presentation.router"]
    config = providers.Singleton(Config)

    # Définir les repositories
    repository_in_memory = providers.Singleton(VaccineRepositoryInMemory)
    repository_in_postgres = providers.Singleton(VaccineRepositoryInPostgres)

    # Définir les repositories pour les epidemics
    epidemic_repository_in_memory = providers.Singleton(EpidemicRepositoryInMemory)
    epidemic_repository_in_postgres = providers.Singleton(EpidemicRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        config.provided.REPOSITORY_TYPE,
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )
    epidemic_repository = providers.Selector(
        config.provided.REPOSITORY_TYPE,
        in_memory=epidemic_repository_in_memory,
        in_postgres=epidemic_repository_in_postgres,
    )

    # Définir les usecases
    add_vaccine_usecase = providers.Factory(
        AddVaccineUseCase,
        repository=repository,
        epidemic_repository=epidemic_repository,
    )
    find_all_vaccines_usecase = providers.Factory(
        FindAllVaccinesUseCase, repository=repository
    )
    find_vaccine_by_id_usecase = providers.Factory(
        FindVaccineByIdUseCase, repository=repository
    )
    update_vaccine_usecase = providers.Factory(
        UpdateVaccineUseCase,
        repository=repository,
        epidemic_repository=epidemic_repository,
    )
    delete_vaccine_usecase = providers.Factory(
        DeleteVaccineUseCase, repository=repository
    )
