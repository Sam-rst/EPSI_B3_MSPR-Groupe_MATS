import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.find_country_by_id_usecase import (
    FindCountryByIdUseCase,
)


class TestFindCountryByIdUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.usecase = FindCountryByIdUseCase(self.country_repository)

    def test_execute_success(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=False)
        self.country_repository.find_by_id.return_value = country

        # Act
        result = self.usecase.execute(1)

        # Assert
        self.country_repository.find_by_id.assert_called_once_with(1)
        assert result == country

    def test_execute_country_not_found(self):
        # Arrange
        self.country_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999)
        assert exc_info.value.status_code == 404
        assert "Le pays n’existe pas" == exc_info.value.detail

    def test_execute_country_deleted(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=True)
        self.country_repository.find_by_id.return_value = country

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1)
        assert exc_info.value.status_code == 400
        assert "Le pays a été supprimé" == exc_info.value.detail
