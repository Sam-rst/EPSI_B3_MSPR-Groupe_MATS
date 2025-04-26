import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.continent.application.usecase.update_continent_usecase import (
    UpdateContinentUseCase,
)
from src.app.continent.presentation.model.payload.update_continent_payload import (
    UpdateContinentPayload,
)


class TestUpdateContinentUseCase:
    def setup_method(self):
        self.continent_repository = Mock()
        self.usecase = UpdateContinentUseCase(self.continent_repository)

    def test_execute_success(self):
        # Arrange
        continent = MagicMock(id=1, name="Europe", is_deleted=False)
        self.continent_repository.find_by_id.return_value = continent

        payload = UpdateContinentPayload(
            name="Europe", code="EU", population=742300000
        )

        # Act
        result = self.usecase.execute(1, payload)

        # Assert
        self.continent_repository.find_by_id.assert_called_once_with(1)
        self.continent_repository.update.assert_called_once_with(continent, payload)
        assert result == continent

    def test_execute_continent_not_found(self):
        # Arrange
        self.continent_repository.find_by_id.return_value = None
        payload = UpdateContinentPayload(name="Europe", code="EU", population=742300000)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999, payload)
        assert exc_info.value.status_code == 404
        assert "Le continent n'existe pas" == exc_info.value.detail

    def test_execute_continent_deleted(self):
        # Arrange
        continent = MagicMock(id=1, name="Europe", is_deleted=True)
        self.continent_repository.find_by_id.return_value = continent

        payload = UpdateContinentPayload(
            name="Europe Updated", code="EU", population=742300000
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1, payload)
        assert exc_info.value.status_code == 400
        assert "Le continent a été supprimé" == exc_info.value.detail

    def test_execute_unexpected_exception(self):
        # Arrange
        continent = MagicMock(id=1, name="Europe", is_deleted=False)
        self.continent_repository.find_by_id.return_value = continent
        
        payload = UpdateContinentPayload(name="Europe", code="EU", population=742300000)
        self.continent_repository.update.side_effect = Exception("Erreur inattendue")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1, payload)
        assert exc_info.value.status_code == 500
        assert "Une erreur inattendue est survenue: Erreur inattendue" == exc_info.value.detail