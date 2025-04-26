import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.add_country_usecase import AddCountryUseCase
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)


class TestAddCountryUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.continent_repository = Mock()
        self.usecase = AddCountryUseCase(
            self.country_repository, self.continent_repository
        )

    def test_execute_success(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )
        self.country_repository.find_by_iso3.return_value = None
        self.continent_repository.find_by_id.return_value = MagicMock()
        self.country_repository.create.return_value = MagicMock(id=1, name="France")

        # Act
        result = self.usecase.execute(payload)

        # Assert
        self.country_repository.find_by_iso3.assert_called_once_with("FRA")
        self.continent_repository.find_by_id.assert_called_once_with(1)
        self.country_repository.create.assert_called_once_with(payload)
        assert result is not None

    def test_execute_duplicate_iso3(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )
        existing_country = MagicMock(is_deleted=False)
        self.country_repository.find_by_iso3.return_value = existing_country

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert "Le code iso3 existe déjà" == exc_info.value.detail

    def test_execute_deleted_country_reactivation(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )
        existing_country = MagicMock(is_deleted=True)
        self.country_repository.find_by_iso3.return_value = existing_country

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert (
            "Le pays existe déjà, il a été supprimé mais il vient d'être restauré."
            == exc_info.value.detail
        )
        self.country_repository.reactivate.assert_called_once_with(existing_country)

    def test_execute_continent_not_found(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=999
        )
        self.country_repository.find_by_iso3.return_value = None
        self.continent_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert (
            "Le continent n'existe pas, veuillez en choisir un autre."
            == exc_info.value.detail
        )
