import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.continent.application.usecase.find_all_continents_usecase import (
    FindAllContinentsUseCase,
)


class TestFindAllContinentsUseCase:
    def setup_method(self):
        self.continent_repository = Mock()
        self.usecase = FindAllContinentsUseCase(self.continent_repository)

    def test_execute_success(self):
        # Arrange
        continents = [MagicMock(id=1, name="Europe"), MagicMock(id=2, name="Asie")]
        self.continent_repository.find_all.return_value = continents

        # Act
        result = self.usecase.execute()

        # Assert
        self.continent_repository.find_all.assert_called_once()
        assert result == continents

    def test_execute_unexpected_exception(self):
        # Arrange
        self.continent_repository.find_all.side_effect = Exception("Erreur inattendue")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute()
        assert exc_info.value.status_code == 500
        assert "Une erreur inattendue est survenue: Erreur inattendue" == exc_info.value.detail