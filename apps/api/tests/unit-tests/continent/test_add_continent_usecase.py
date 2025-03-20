import unittest
from unittest.mock import Mock
from fastapi import HTTPException
from src.app.continent.application.usecase.add_continent_usecase import (
    AddContinentUseCase,
)
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.infrastructure.repository.continent_repo_in_memory import (
    ContinentRepositoryInMemory,
)

class TestAddContinentUseCase(unittest.TestCase):

    def setUp(self):
        self.mock_repository = Mock(spec=ContinentRepositoryInMemory)
        self.usecase = AddContinentUseCase(repository=self.mock_repository)

    def test_add_continent_success(self):
        payload = CreateContinentPayload(code="AFR", name="Africa", population=1000)
        self.mock_repository.find_by_code.return_value = None
        self.mock_repository.create.return_value = ContinentEntity(
            code="AFR", name="Africa", population=1000
        )

        result = self.usecase.execute(payload)

        self.assertEqual(result.code, "AFR")
        self.assertEqual(result.name, "Africa")
        self.assertEqual(result.population, 1000)
        # self.mock_repository.find_by_code.assert_called_once_with("AFR")
        # self.mock_repository.create.assert_called_once_with(payload)


if __name__ == "__main__":
    unittest.main()
