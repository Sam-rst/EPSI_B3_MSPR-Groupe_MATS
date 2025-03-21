import unittest
from unittest.mock import MagicMock
from src.app.continent.application.usecase.update_continent_usecase import UpdateContinentUseCase
from src.app.continent.presentation.model.payload.update_continent_payload import UpdateContinentPayload
from src.app.continent.domain.entity.continent_entity import ContinentEntity
from src.app.continent.domain.interface.continent_repository import ContinentRepository

class TestUpdateContinentUseCase(unittest.TestCase):

    def setUp(self):
        self.repository = MagicMock(spec=ContinentRepository)
        self.usecase = UpdateContinentUseCase(self.repository)

    def test_update_continent_success(self):
        payload = UpdateContinentPayload(name="Updated Africa", code="AF", population=1300000000)
        existing_continent = ContinentEntity(name="Africa", code="AF", population=1200000000)
        self.repository.find_by_id.return_value = existing_continent

        updated_continent = self.usecase.execute(existing_continent.id, payload)

        self.repository.find_by_id.assert_called_once_with(existing_continent.id)
        self.repository.update.assert_called_once()
        self.assertEqual(updated_continent.name, "Updated Africa")
        self.assertEqual(updated_continent.code, "AF")
        self.assertEqual(updated_continent.population, 1300000000)

    def test_update_continent_not_found(self):
        payload = UpdateContinentPayload(name="Updated Africa", code="AF", population=1300000000)
        self.repository.find_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            self.usecase.execute(999, payload)

        self.assertEqual(str(context.exception), "Le continent n'existe pas")

if __name__ == '__main__':
    unittest.main()