from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.country.domain.interface.country_repository import CountryRepository
from src.app.country.domain.entity.country_entity import CountryEntity
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

    def update(self, id: int, payload: UpdateCountryPayload) -> Optional[CountryModel]:
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if not model:
            return None  # Le pays n'existe pas

        # Mise à jour des champs
        model.name = payload.name
        model.iso2 = payload.iso2
        model.iso3 = payload.iso3
        model.population = payload.population

        self.session.commit()
        # return CountryMappingUtils.model_to_entity(model)

    def delete(self, id: int) -> Optional[CountryEntity]:
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            # return CountryMappingUtils.model_to_entity(model)
        return None

    def find_by_id(self, id: int) -> Optional[CountryEntity]:
        model = self.session.query(CountryModel).filter(CountryModel.id == id).first()
        if model:
            return model
        return None

    def find_by_iso3(self, iso3: str) -> Optional[CountryEntity]:
        model = (
            self.session.query(CountryModel).filter(CountryModel.iso3 == iso3).first()
        )
        if model:
            return model
        return None

    def find_all(self) -> List[CountryEntity]:
        models = self.session.query(CountryModel).all()
        # return [CountryMappingUtils.model_to_entity(model) for model in models]
