from src.app.continent.domain.interface.continent_repository import ContinentRepository
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


class ContinentRepositoriesContainer:
    _continent_repository_in_memory: ContinentRepository = None
    _continent_repository_in_postgres: ContinentRepository = None

    @staticmethod
    def get_repository_in_memory() -> ContinentRepository:
        if not ContinentRepositoriesContainer._continent_repository_in_memory:
            ContinentRepositoriesContainer._continent_repository_in_memory = (
                ContinentRepositoryInMemory()
            )
        return ContinentRepositoriesContainer._continent_repository_in_memory

    @staticmethod
    def get_repository_in_postgres() -> ContinentRepository:
        if not ContinentRepositoriesContainer._continent_repository_in_postgres:
            ContinentRepositoriesContainer._continent_repository_in_postgres = (
                ContinentRepositoryInPostgres()
            )
        return ContinentRepositoriesContainer._continent_repository_in_postgres


class ContinentUseCasesContainer:
    _add_continent_usecase: AddContinentUseCase = None
    _find_all_continents_usecase: FindAllContinentsUseCase = None

    @staticmethod
    def get_add_continent_usecase(repository: ContinentRepository) -> AddContinentUseCase:
        if not ContinentUseCasesContainer._add_continent_usecase:
            ContinentUseCasesContainer._add_continent_usecase = (
                AddContinentUseCase(repository)
            )
        return ContinentUseCasesContainer._add_continent_usecase

    @staticmethod
    def get_find_all_continents_usecase(repository: ContinentRepository) -> FindAllContinentsUseCase:
        if not ContinentUseCasesContainer._find_all_continents_usecase:
            ContinentUseCasesContainer._find_all_continents_usecase = (
                FindAllContinentsUseCase(repository)
            )
        return ContinentUseCasesContainer._find_all_continents_usecase

class ContinentContainer:
    _continent_repositories_container: ContinentRepositoriesContainer = None
    _continent_usecases_container: ContinentUseCasesContainer = None

    @staticmethod
    def get_repositories_container() -> ContinentRepositoriesContainer:
        if not ContinentContainer._continent_repositories_container:
            ContinentContainer._continent_repositories_container = (
                ContinentRepositoriesContainer()
            )
        return ContinentContainer._continent_repositories_container

    @staticmethod
    def get_usecases_container() -> ContinentUseCasesContainer:
        if not ContinentContainer._continent_usecases_container:
            ContinentContainer._continent_usecases_container = (
                ContinentUseCasesContainer()
            )
        return ContinentContainer._continent_usecases_container