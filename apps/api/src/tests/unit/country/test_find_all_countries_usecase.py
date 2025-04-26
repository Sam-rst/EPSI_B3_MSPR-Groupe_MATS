from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.find_all_countries_usecase import (
    FindAllCountriesUseCase,
)


class TestFindAllCountriesUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.usecase = FindAllCountriesUseCase(self.country_repository)

    def test_execute_success(self):
        # Arrange
        countries = [MagicMock(id=1, name="France"), MagicMock(id=2, name="Germany")]
        self.country_repository.find_all.return_value = countries

        # Act
        result = self.usecase.execute()

        # Assert
        self.country_repository.find_all.assert_called_once()
        assert result == countries
