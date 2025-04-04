from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.vaccine.presentation.model.payload.create_vaccine_payload import (
    CreateVaccinePayload,
)
from src.app.vaccine.presentation.model.payload.update_vaccine_payload import (
    UpdateVaccinePayload,
)


class VaccineRepositoryInPostgres(VaccineRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateVaccinePayload) -> VaccineModel:
        try:
            model = VaccineModel(
                name=payload.name,
                laboratory=payload.laboratory,
                technology=payload.technology,
                dose=payload.dose,
                efficacy=payload.efficacy,
                storage_temperature=payload.storage_temperature,
                epidemic_id=payload.epidemic_id,
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, vaccine: VaccineModel, payload: UpdateVaccinePayload
    ) -> Optional[VaccineModel]:
        try:
            if payload.name is not None:
                vaccine.name = payload.name
            if payload.laboratory is not None:
                vaccine.laboratory = payload.laboratory
            if payload.technology is not None:
                vaccine.technology = payload.technology
            if payload.dose is not None:
                vaccine.dose = payload.dose
            if payload.efficacy is not None:
                vaccine.efficacy = payload.efficacy
            if payload.storage_temperature is not None:
                vaccine.storage_temperature = payload.storage_temperature
            if payload.epidemic_id is not None:
                vaccine.epidemic_id = payload.epidemic_id
            vaccine.update("system")
            self.session.commit()

            return vaccine
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, vaccine: VaccineModel) -> Optional[VaccineModel]:
        try:
            vaccine.delete("system")
            self.session.commit()

            return vaccine
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[VaccineModel]:
        try:
            vaccine = (
                self.session.query(VaccineModel).filter(VaccineModel.id == id).first()
            )

            return vaccine
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_name(self, name: str) -> Optional[VaccineModel]:
        try:
            vaccine = (
                self.session.query(VaccineModel)
                .filter(VaccineModel.name == name)
                .first()
            )

            return vaccine
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[VaccineModel]:
        try:
            vaccines = (
                self.session.query(VaccineModel)
                .filter(VaccineModel.is_deleted == False)
                .all()
            )

            return vaccines
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, vaccine: VaccineModel) -> VaccineModel:
        try:
            vaccine.reactivate("system")
            self.session.commit()
            return vaccine
        except Exception as e:
            self.session.rollback()
            raise e
