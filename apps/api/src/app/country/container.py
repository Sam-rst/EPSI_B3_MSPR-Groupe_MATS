from dependency_injector import containers, providers

from src.config.config import Config

from src.app.country.infrastructure.repository.country_repo_in_memory import (
    CountryRepositoryInMemory,
)
from src.app.country.infrastructure.repository.country_repo_in_postgres import (
    CountryRepositoryInPostgres,
)
from src.app.country.application.usecase.add_country_usecase import (
    AddCountryUseCase,
)
from src.app.country.application.usecase.find_all_countries_usecase import (
    FindAllCountriesUseCase,
)
from src.app.country.application.usecase.find_country_by_id_usecase import (
    FindCountryByIdUseCase,
)
from src.app.country.application.usecase.update_country_usecase import (
    UpdateCountryUseCase,
)
from src.app.country.application.usecase.delete_country_usecase import (
    DeleteCountryUseCase,
)


class CountryContainer(containers.DeclarativeContainer):
    modules = ["src.app.country.presentation.router"]
    config = providers.Singleton(Config)

    # Définir les repositories
    repository_in_memory = providers.Singleton(CountryRepositoryInMemory)
    repository_in_postgres = providers.Singleton(CountryRepositoryInPostgres)

    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        config.provided.REPOSITORY_TYPE,
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    add_country_usecase = providers.Factory(
        AddCountryUseCase, repository=repository
    )
    find_all_countries_usecase = providers.Factory(
        FindAllCountriesUseCase, repository=repository
    )
    find_country_by_id_usecase = providers.Factory(
        FindCountryByIdUseCase, repository=repository
    )
    update_country_usecase = providers.Factory(
        UpdateCountryUseCase, repository=repository
    )
    delete_country_usecase = providers.Factory(
        DeleteCountryUseCase, repository=repository
    )