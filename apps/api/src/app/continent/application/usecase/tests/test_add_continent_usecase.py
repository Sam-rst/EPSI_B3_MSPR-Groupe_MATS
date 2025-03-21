import unittest
from unittest.mock import MagicMock
from src.app.continent.application.usecase.add_continent_usecase import AddContinentUseCase
from src.app.continent.presentation.model.payload.create_continent_payload import CreateContinentPayload
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.domain.interface.continent_repository import ContinentRepository

class TestAddContinentUseCase(unittest.TestCase):

    def setUp(self):
        self.repository = MagicMock(spec=ContinentRepository)
        self.usecase = AddContinentUseCase(self.repository)

    def test_add_continent_success(self):
        payload = CreateContinentPayload(name="Africa", code="AFR", population=1200000000)
        self.repository.find_by_code.return_value = None
        self.repository.create.return_value = ContinentEntity(name="Africa", code="AFR", population=1200000000)

        continent = self.usecase.execute(payload)

        self.repository.find_by_code.assert_called_once_with("AFR")
        self.repository.create.assert_called_once()
        self.assertEqual(continent.name, "Africa")
        self.assertEqual(continent.code, "AFR")
        self.assertEqual(continent.population, 1200000000)

    def test_add_continent_existing_code(self):
        payload = CreateContinentPayload(name="Africa", code="AFR", population=1200000000)
        existing_continent = ContinentEntity(name="Africa", code="AFR", population=1200000000)
        self.repository.find_by_code.return_value = existing_continent

        with self.assertRaises(ValueError) as context:
            self.usecase.execute(payload)

        self.assertEqual(str(context.exception), "Le code continent existe déjà")

if __name__ == '__main__':
    unittest.main()