from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.country.presentation.model.payload.create_country_payload import (
    CreateCountryPayload,
)
from src.app.country.presentation.model.payload.update_country_payload import (
    UpdateCountryPayload,
)


class CountryRepositoryInPostgres(CountryRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateCountryPayload) -> CountryModel:
        try:
            model = CountryModel(
                name=payload.name,
                iso2=payload.iso2,
                iso3=payload.iso3,
                population=payload.population,
                continent_id=payload.continent_id,
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, country: CountryModel, payload: UpdateCountryPayload
    ) -> Optional[CountryModel]:
        try:
            if payload.name is not None:
                country.name = payload.name
            if payload.iso2 is not None:
                country.iso2 = payload.iso2
            if payload.iso3 is not None:
                country.iso3 = payload.iso3
            if payload.population is not None:
                country.population = payload.population
            if payload.continent_id is not None:
                country.continent_id = payload.continent_id
            country.update("system")
            self.session.commit()

            return country
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, country: CountryModel) -> Optional[CountryModel]:
        try:
            country.delete("system")
            self.session.commit()

            return country
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[CountryModel]:
        try:
            country = (
                self.session.query(CountryModel).filter(CountryModel.id == id).first()
            )

            return country
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_iso3(self, iso3: str) -> Optional[CountryModel]:
        try:
            country = (
                self.session.query(CountryModel)
                .filter(CountryModel.iso3 == iso3)
                .first()
            )

            return country
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[CountryModel]:
        """_summary_

        Raises:
            e: _description_

        Returns:
            List[CountryModel]: _description_
        """
        try:
            countries = (
                self.session.query(CountryModel)
                .filter(CountryModel.is_deleted == False)
                .all()
            )

            return countries
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, country: CountryModel) -> CountryModel:
        try:
            country.reactivate("system")
            self.session.commit()
            return country
        except Exception as e:
            self.session.rollback()
            raise e
