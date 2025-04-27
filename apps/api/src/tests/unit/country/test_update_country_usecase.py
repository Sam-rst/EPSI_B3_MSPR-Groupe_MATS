import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.update_country_usecase import (
    UpdateCountryUseCase,
)
from src.app.country.presentation.model.payload.update_country_payload import (
    UpdateCountryPayload,
)


class TestUpdateCountryUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.continent_repository = Mock()
        self.usecase = UpdateCountryUseCase(
            self.country_repository, self.continent_repository
        )

    def test_execute_success(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=False)
        self.country_repository.find_by_id.return_value = country

        continent = MagicMock(id=1, is_deleted=False)
        self.continent_repository.find_by_id.return_value = continent

        payload = UpdateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )

        # Act
        result = self.usecase.execute(1, payload)

        # Assert
        self.country_repository.find_by_id.assert_called_once_with(1)
        self.continent_repository.find_by_id.assert_called_once_with(1)
        self.country_repository.update.assert_called_once_with(country, payload)
        assert result == country

    def test_execute_country_not_found(self):
        # Arrange
        self.country_repository.find_by_id.return_value = None
        payload = UpdateCountryPayload(name="France")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999, payload)
        assert exc_info.value.status_code == 404
        assert "Le pays n'existe pas" == exc_info.value.detail

    def test_execute_country_deleted(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=True)
        self.country_repository.find_by_id.return_value = country

        # Créer un payload complet avec tous les champs
        payload = UpdateCountryPayload(
            name="France Updated",
            iso2="FR",
            iso3="FRA",
            population=67000000,
            continent_id=1,
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1, payload)
        assert exc_info.value.status_code == 400
        assert "Le pays a été supprimé" == exc_info.value.detail

    def test_execute_country_not_found(self):
        # Arrange
        self.country_repository.find_by_id.return_value = None

        # Créer un payload complet avec tous les champs
        payload = UpdateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999, payload)
        assert exc_info.value.status_code == 404
        assert "Le pays n'existe pas" == exc_info.value.detail

    def test_execute_continent_deleted(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=False)
        self.country_repository.find_by_id.return_value = country

        continent = MagicMock(id=1, is_deleted=True)
        self.continent_repository.find_by_id.return_value = continent

        # Créer un payload complet avec tous les champs
        payload = UpdateCountryPayload(
            name="France", iso2="FR", iso3="FRA", population=67000000, continent_id=1
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999, payload)
        assert exc_info.value.status_code == 400
        assert (
            "Le continent a été supprimé, veuillez choisir un autre continent"
            == exc_info.value.detail
        )
