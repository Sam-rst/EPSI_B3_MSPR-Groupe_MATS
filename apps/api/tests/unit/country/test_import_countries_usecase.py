import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.import_countries_usecase import (
    ImportCountriesUseCase,
)
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)


class TestImportCountriesUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.continent_repository = Mock()
        self.usecase = ImportCountriesUseCase(
            self.country_repository, self.continent_repository
        )

    def test_execute_all_success(self):
        # Arrange
        payloads = [
            CreateCountryPayload(
                name="France",
                iso2="FR",
                iso3="FRA",
                population=67000000,
                continent_id=1,
            ),
            CreateCountryPayload(
                name="Germany",
                iso2="DE",
                iso3="DEU",
                population=83000000,
                continent_id=1,
            ),
        ]

        self.country_repository.find_by_iso3.return_value = None
        self.continent_repository.find_by_id.return_value = MagicMock()
        self.country_repository.create.return_value = MagicMock()

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 2
        assert len(result.errors) == 0
        assert self.country_repository.find_by_iso3.call_count == 2
        assert self.continent_repository.find_by_id.call_count == 2
        assert self.country_repository.create.call_count == 2
        assert result.success[0].iso3 == "FRA"
        assert result.success[0].status == "created"
        assert result.success[1].iso3 == "DEU"
        assert result.success[1].status == "created"

    def test_execute_with_existing_countries(self):
        # Arrange
        payloads = [
            CreateCountryPayload(
                name="France",
                iso2="FR",
                iso3="FRA",
                population=67000000,
                continent_id=1,
            ),
            CreateCountryPayload(
                name="Germany",
                iso2="DE",
                iso3="DEU",
                population=83000000,
                continent_id=1,
            ),
        ]

        existing_country = MagicMock(is_deleted=False)
        self.country_repository.find_by_iso3.side_effect = [existing_country, None]
        self.continent_repository.find_by_id.return_value = MagicMock()
        self.country_repository.create.return_value = MagicMock()

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 1
        assert len(result.errors) == 1
        assert result.errors[0].iso3 == "FRA"
        assert "Le nom du pays existe déjà" in result.errors[0].error
        assert result.success[0].iso3 == "DEU"
        assert result.success[0].status == "created"

    def test_execute_with_deleted_countries(self):
        # Arrange
        payloads = [
            CreateCountryPayload(
                name="France",
                iso2="FR",
                iso3="FRA",
                population=67000000,
                continent_id=1,
            ),
        ]

        deleted_country = MagicMock(is_deleted=True)
        self.country_repository.find_by_iso3.return_value = deleted_country

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 1
        assert len(result.errors) == 0
        assert result.success[0].iso3 == "FRA"
        assert result.success[0].status == "reactivated"
        self.country_repository.reactivate.assert_called_once_with(deleted_country)

    def test_execute_with_nonexistent_continent(self):
        # Arrange
        payloads = [
            CreateCountryPayload(
                name="France",
                iso2="FR",
                iso3="FRA",
                population=67000000,
                continent_id=999,
            ),
        ]

        self.country_repository.find_by_iso3.return_value = None
        self.continent_repository.find_by_id.return_value = None

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 0
        assert len(result.errors) == 1
        assert result.errors[0].iso3 == "FRA"
        assert "Le continent n'existe pas" in result.errors[0].error

    def test_execute_mixed_scenarios(self):
        # Arrange
        payloads = [
            CreateCountryPayload(
                name="France",
                iso2="FR",
                iso3="FRA",
                population=67000000,
                continent_id=1,
            ),  # Existing, not deleted
            CreateCountryPayload(
                name="Germany",
                iso2="DE",
                iso3="DEU",
                population=83000000,
                continent_id=1,
            ),  # New country
            CreateCountryPayload(
                name="Italy", iso2="IT", iso3="ITA", population=60000000, continent_id=1
            ),  # Deleted country
            CreateCountryPayload(
                name="Unknown", iso2="XX", iso3="XXX", population=0, continent_id=999
            ),  # Non-existent continent
        ]

        existing_country = MagicMock(is_deleted=False)
        deleted_country = MagicMock(is_deleted=True)

        self.country_repository.find_by_iso3.side_effect = [
            existing_country,  # France
            None,  # Germany
            deleted_country,  # Italy
            None,  # Unknown
        ]

        self.continent_repository.find_by_id.side_effect = [
            MagicMock(),  # For Germany
            None,  # For Unknown
        ]

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 2
        assert len(result.errors) == 2

        # Verify errors
        error_isos = [error.iso3 for error in result.errors]
        assert "FRA" in error_isos
        assert "XXX" in error_isos

        # Verify successes
        success_isos = [success.iso3 for success in result.success]
        assert "DEU" in success_isos
        assert "ITA" in success_isos

        # Verify status
        for success in result.success:
            if success.iso3 == "DEU":
                assert success.status == "created"
            elif success.iso3 == "ITA":
                assert success.status == "reactivated"
