import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.continent.application.usecase.add_continent_usecase import AddContinentUseCase
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)


class TestAddContinentUseCase:
    def setup_method(self):
        self.continent_repository = Mock()
        self.usecase = AddContinentUseCase(self.continent_repository)

    def test_execute_success(self):
        # Arrange
        payload = CreateContinentPayload(
            name="Europe", code="EU", population=742300000
        )
        self.continent_repository.find_by_code.return_value = None
        self.continent_repository.create.return_value = MagicMock(id=1, name="Europe")

        # Act
        result = self.usecase.execute(payload)

        # Assert
        self.continent_repository.find_by_code.assert_called_once_with("EU")
        self.continent_repository.create.assert_called_once_with(payload)
        assert result is not None

    def test_execute_duplicate_code(self):
        # Arrange
        payload = CreateContinentPayload(
            name="Europe", code="EU", population=742300000
        )
        existing_continent = MagicMock(is_deleted=False)
        self.continent_repository.find_by_code.return_value = existing_continent

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert "Le code continent existe déjà" == exc_info.value.detail

    def test_execute_deleted_continent_reactivation(self):
        # Arrange
        payload = CreateContinentPayload(
            name="Europe", code="EU", population=742300000
        )
        existing_continent = MagicMock(is_deleted=True)
        self.continent_repository.find_by_code.return_value = existing_continent

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert (
            "Le continent existe déjà, il a été supprimé mais il vient d'être restauré."
            == exc_info.value.detail
        )
        self.continent_repository.reactivate.assert_called_once_with(existing_continent)

    def test_execute_unexpected_exception(self):
        # Arrange
        payload = CreateContinentPayload(
            name="Europe", code="EU", population=742300000
        )
        self.continent_repository.find_by_code.side_effect = Exception("Erreur inattendue")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 500
        assert "Une erreur inattendue est survenue: Erreur inattendue" == exc_info.value.detail