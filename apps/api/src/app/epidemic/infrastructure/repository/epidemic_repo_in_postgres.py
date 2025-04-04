from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.epidemic.domain.interface.epidemic_repository import EpidemicRepository
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.epidemic.presentation.model.payload.create_epidemic_payload import (
    CreateEpidemicPayload,
)
from src.app.epidemic.presentation.model.payload.update_epidemic_payload import (
    UpdateEpidemicPayload,
)


class EpidemicRepositoryInPostgres(EpidemicRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateEpidemicPayload) -> EpidemicModel:
        try:
            model = EpidemicModel(
                name=payload.name,
                start_date=payload.start_date,
                end_date=payload.end_date,
                type=payload.type,
                pathogen_name=payload.pathogen_name,
                description=payload.description,
                transmission_mode=payload.transmission_mode,
                symptoms=payload.symptoms,
                reproduction_rate=payload.reproduction_rate,
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, epidemic: EpidemicModel, payload: UpdateEpidemicPayload
    ) -> Optional[EpidemicModel]:
        try:
            if payload.name:
                epidemic.name = payload.name
            if payload.start_date:
                epidemic.start_date = payload.start_date
            if payload.end_date:
                epidemic.end_date = payload.end_date
            if payload.type:
                epidemic.type = payload.type
            if payload.pathogen_name:
                epidemic.pathogen_name = payload.pathogen_name
            if payload.description:
                epidemic.description = payload.description
            if payload.transmission_mode:
                epidemic.transmission_mode = payload.transmission_mode
            if payload.symptoms:
                epidemic.symptoms = payload.symptoms
            if payload.reproduction_rate:
                epidemic.reproduction_rate = payload.reproduction_rate
            epidemic.update("system")
            self.session.commit()

            return epidemic
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, epidemic: EpidemicModel) -> Optional[EpidemicModel]:
        try:
            epidemic.delete("system")
            self.session.commit()

            return epidemic
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[EpidemicModel]:
        try:
            epidemic = (
                self.session.query(EpidemicModel).filter(EpidemicModel.id == id).first()
            )

            return epidemic
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_name(self, name: str) -> Optional[EpidemicModel]:
        try:
            epidemic = (
                self.session.query(EpidemicModel)
                .filter(EpidemicModel.name == name)
                .first()
            )

            return epidemic
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[EpidemicModel]:
        """_summary_

        Raises:
            e: _description_

        Returns:
            List[EpidemicModel]: _description_
        """
        try:
            epidemics = (
                self.session.query(EpidemicModel)
                .filter(EpidemicModel.is_deleted == False)
                .all()
            )

            return epidemics
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, epidemic: EpidemicModel) -> EpidemicModel:
        try:
            epidemic.reactivate("system")
            self.session.commit()
            return epidemic
        except Exception as e:
            self.session.rollback()
            raise e
