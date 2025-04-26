import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.continent.application.usecase.find_continent_by_id_usecase import (
    FindContinentByIdUseCase,
)


class TestFindContinentByIdUseCase:
    def setup_method(self):
        self.continent_repository = Mock()
        self.usecase = FindContinentByIdUseCase(self.continent_repository)

    def test_execute_success(self):
        # Arrange
        continent = MagicMock(id=1, name="Europe", is_deleted=False)
        self.continent_repository.find_by_id.return_value = continent

        # Act
        result = self.usecase.execute(1)

        # Assert
        self.continent_repository.find_by_id.assert_called_once_with(1)
        assert result == continent

    def test_execute_continent_not_found(self):
        # Arrange
        self.continent_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999)
        assert exc_info.value.status_code == 404
        assert "Le continent n’existe pas" == exc_info.value.detail

    def test_execute_continent_deleted(self):
        # Arrange
        continent = MagicMock(id=1, name="Europe", is_deleted=True)
        self.continent_repository.find_by_id.return_value = continent

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1)
        assert exc_info.value.status_code == 400
        assert "Le continent a été supprimé" == exc_info.value.detail

    def test_execute_unexpected_exception(self):
        # Arrange
        self.continent_repository.find_by_id.side_effect = Exception("Erreur inattendue")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1)
        assert exc_info.value.status_code == 500
        assert "Une erreur inattendue est survenue: Erreur inattendue" == exc_info.value.detail