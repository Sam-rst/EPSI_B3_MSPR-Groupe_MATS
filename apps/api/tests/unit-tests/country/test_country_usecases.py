import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from src.app.country.application.usecase.add_country_usecase import AddCountryUseCase
from src.app.country.application.usecase.find_all_countries_usecase import FindAllCountriesUseCase
from src.app.country.application.usecase.find_country_by_id_usecase import FindCountryByIdUseCase
from src.app.country.application.usecase.update_country_usecase import UpdateCountryUseCase
from src.app.country.application.usecase.delete_country_usecase import DeleteCountryUseCase
from src.app.country.presentation.model.payload.create_country_payload import CreateCountryPayload
from src.app.country.presentation.model.payload.update_country_payload import UpdateCountryPayload
from src.app.country.domain.entity.country_entity import CountryEntity
from src.app.country.infrastructure.model.country_model import CountryModel


class TestAddCountryUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.continent_repository = Mock()
        self.usecase = AddCountryUseCase(self.country_repository, self.continent_repository)

    def test_execute_success(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", 
            iso2="FR", 
            iso3="FRA", 
            population=67000000, 
            continent_id=1
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
            name="France", 
            iso2="FR", 
            iso3="FRA", 
            population=67000000, 
            continent_id=1
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
            name="France", 
            iso2="FR", 
            iso3="FRA", 
            population=67000000, 
            continent_id=1
        )
        existing_country = MagicMock(is_deleted=True)
        self.country_repository.find_by_iso3.return_value = existing_country

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert "Le pays existe déjà, il a été supprimé mais il vient d'être restauré." == exc_info.value.detail
        self.country_repository.reactivate.assert_called_once_with(existing_country)

    def test_execute_continent_not_found(self):
        # Arrange
        payload = CreateCountryPayload(
            name="France", 
            iso2="FR", 
            iso3="FRA", 
            population=67000000, 
            continent_id=999
        )
        self.country_repository.find_by_iso3.return_value = None
        self.continent_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(payload)
        assert exc_info.value.status_code == 400
        assert "Le continent n'existe pas, veuillez en choisir un autre." == exc_info.value.detail


class TestFindAllCountriesUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.usecase = FindAllCountriesUseCase(self.country_repository)

    def test_execute_success(self):
        # Arrange
        countries = [
            MagicMock(id=1, name="France"),
            MagicMock(id=2, name="Germany")
        ]
        self.country_repository.find_all.return_value = countries

        # Act
        result = self.usecase.execute()

        # Assert
        self.country_repository.find_all.assert_called_once()
        assert result == countries


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


class TestUpdateCountryUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.continent_repository = Mock()
        self.usecase = UpdateCountryUseCase(self.country_repository, self.continent_repository)

    def test_execute_success(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=False)
        self.country_repository.find_by_id.return_value = country
        
        continent = MagicMock(id=1, is_deleted=False)
        self.continent_repository.find_by_id.return_value = continent
        
        payload = UpdateCountryPayload(
            name="France", 
            iso2="FR", 
            iso3="FRA", 
            population=67000000, 
            continent_id=1
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
            continent_id=1
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
            name="France",
            iso2="FR",
            iso3="FRA",
            population=67000000,
            continent_id=1
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
            name="France",
            iso2="FR",
            iso3="FRA",
            population=67000000,
            continent_id=1
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999, payload)
        assert exc_info.value.status_code == 400
        assert "Le continent a été supprimé, veuillez choisir un autre continent" == exc_info.value.detail


class TestDeleteCountryUseCase:
    def setup_method(self):
        self.country_repository = Mock()
        self.usecase = DeleteCountryUseCase(self.country_repository)

    def test_execute_success(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=False)
        self.country_repository.find_by_id.return_value = country
        self.country_repository.delete.return_value = country

        # Act
        result = self.usecase.execute(1)

        # Assert
        self.country_repository.find_by_id.assert_called_once_with(1)
        self.country_repository.delete.assert_called_once_with(country)
        assert result == country

    def test_execute_country_not_found(self):
        # Arrange
        self.country_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(999)
        assert exc_info.value.status_code == 404
        assert "Le pays n'existe pas" == exc_info.value.detail

    def test_execute_country_already_deleted(self):
        # Arrange
        country = MagicMock(id=1, name="France", is_deleted=True)
        self.country_repository.find_by_id.return_value = country

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.usecase.execute(1)
        assert exc_info.value.status_code == 400
        assert "Le pays a déjà été supprimé" == exc_info.value.detail