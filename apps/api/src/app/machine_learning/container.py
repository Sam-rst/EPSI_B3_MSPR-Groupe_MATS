from src.app.machine_learning.application.usecase.ask_prediction_to_machine_learning_usecase import AskPredictionToMachineLearningUseCase
from src.app.machine_learning.application.usecase.export_data_for_machine_learning_usecase import ExportDataForMachineLearningUseCase
from src.app.machine_learning.infrastructure.repository.machine_learning_repo_in_memory import MachineLearningRepositoryInMemory
from src.app.machine_learning.infrastructure.repository.machine_learning_repo_in_postgres import MachineLearningRepositoryInPostgres
from dependency_injector import containers, providers

from src.core.config import settings




class MachineLearningContainer(containers.DeclarativeContainer):
    modules = ["src.app.machine_learning.presentation.router"]

    # Définir les repositories
    repository_in_memory = providers.Singleton(MachineLearningRepositoryInMemory)
    repository_in_postgres = providers.Singleton(MachineLearningRepositoryInPostgres)


    # Sélectionner le repository en fonction de la configuration
    repository = providers.Selector(
        lambda: settings.REPOSITORY_TYPE.lower(),
        in_memory=repository_in_memory,
        in_postgres=repository_in_postgres,
    )

    # Définir les usecases
    ask_prediction_to_machine_learning_usecase = providers.Factory(
        AskPredictionToMachineLearningUseCase,
        repository=repository
    )
    export_data_for_machine_learning_usecase = providers.Factory(
        ExportDataForMachineLearningUseCase,
        repository=repository
    )