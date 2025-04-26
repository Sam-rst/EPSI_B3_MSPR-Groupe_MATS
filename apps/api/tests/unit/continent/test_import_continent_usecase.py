import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.continent.application.usecase.import_continents_usecase import (
    ImportContinentsUseCase,
)
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)


class TestImportContinentsUseCase:
    def setup_method(self):
        self.continent_repository = Mock()
        self.usecase = ImportContinentsUseCase(self.continent_repository)

    def test_execute_all_success(self):
        # Arrange
        payloads = [
            CreateContinentPayload(name="Europe", code="EU", population=742300000),
            CreateContinentPayload(name="Asie", code="AS", population=4830000000),
        ]

        self.continent_repository.find_by_code.return_value = None
        self.continent_repository.create.return_value = MagicMock()

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 2
        assert len(result.errors) == 0
        assert self.continent_repository.find_by_code.call_count == 2
        assert self.continent_repository.create.call_count == 2
        assert result.success[0].code == "EU"
        assert result.success[0].status == "created"
        assert result.success[1].code == "AS"
        assert result.success[1].status == "created"

    def test_execute_with_existing_continents(self):
        # Arrange
        payloads = [
            CreateContinentPayload(name="Europe", code="EU", population=742300000),
            CreateContinentPayload(name="Asie", code="AS", population=4830000000),
        ]

        existing_continent = MagicMock(is_deleted=False)
        self.continent_repository.find_by_code.side_effect = [existing_continent, None]
        self.continent_repository.create.return_value = MagicMock()

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 1
        assert len(result.errors) == 1
        assert result.errors[0].code == "EU"
        assert "Le code continent existe déjà" == result.errors[0].error
        assert result.success[0].code == "AS"
        assert result.success[0].status == "created"

    def test_execute_with_deleted_continents(self):
        # Arrange
        payloads = [
            CreateContinentPayload(name="Europe", code="EU", population=742300000),
        ]

        deleted_continent = MagicMock(is_deleted=True)
        self.continent_repository.find_by_code.return_value = deleted_continent

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 1
        assert len(result.errors) == 0
        assert result.success[0].code == "EU"
        assert result.success[0].status == "reactivated"
        self.continent_repository.reactivate.assert_called_once_with(deleted_continent)

    def test_execute_mixed_scenarios(self):
        # Arrange
        payloads = [
            CreateContinentPayload(name="Europe", code="EU", population=742300000),  # Existing, not deleted
            CreateContinentPayload(name="Asie", code="AS", population=4830000000),    # New continent
            CreateContinentPayload(name="Amérique", code="AM", population=332180000),  # Deleted continent
        ]

        existing_continent = MagicMock(is_deleted=False)
        deleted_continent = MagicMock(is_deleted=True)

        self.continent_repository.find_by_code.side_effect = [
            existing_continent,  # Europe
            None,               # Asie
            deleted_continent,  # Amérique
        ]

        # Act
        result = self.usecase.execute(payloads)

        # Assert
        assert len(result.success) == 2
        assert len(result.errors) == 1

        # Verify errors
        assert result.errors[0].code == "EU"
        assert "Le code continent existe déjà" == result.errors[0].error

        # Verify successes
        success_codes = [success.code for success in result.success]
        assert "AS" in success_codes
        assert "AM" in success_codes

        # Verify status
        for success in result.success:
            if success.code == "AS":
                assert success.status == "created"
            elif success.code == "AM":
                assert success.status == "reactivated"

    def test_execute_unexpected_exception(self):
        # Arrange
        payloads = [CreateContinentPayload(name="Europe", code="EU", population=742300000)]
        self.continent_repository.find_by_code.side_effect = Exception("Erreur inattendue")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payloads)
        assert exc_info.value.status_code == 500
        assert "Une erreur inattendue est survenue: Erreur inattendue" == exc_info.value.detail