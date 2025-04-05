from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.continent.domain.interface.continent_repository import ContinentRepository
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.continent.presentation.model.payload.create_continent_payload import (
    CreateContinentPayload,
)
from src.app.continent.presentation.model.payload.update_continent_payload import (
    UpdateContinentPayload,
)


class ContinentRepositoryInPostgres(ContinentRepository):
    def __init__(self):
        """
        Initialise le repository avec une session SQLAlchemy.

        Args:
            session (Session): La session SQLAlchemy pour interagir avec la base de données.
        """
        self._session = db.get_session()

    @property
    def session(self) -> Session:
        return self._session

    def create(self, payload: CreateContinentPayload) -> ContinentModel:
        """_summary_

        Args:
            payload (CreateContinentPayload): _description_

        Raises:
            e: _description_

        Returns:
            ContinentModel: _description_
        """
        try:
            model = ContinentModel(
                name=payload.name, code=payload.code, population=payload.population
            )
            self.session.add(model)
            self.session.commit()

            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, continent: ContinentModel, payload: UpdateContinentPayload
    ) -> ContinentModel:
        """_summary_

        Args:
            continent (ContinentModel): _description_
            payload (UpdateContinentPayload): _description_

        Raises:
            e: _description_

        Returns:
            ContinentModel: _description_
        """
        try:
            if payload.name is not None:
                continent.name = payload.name
            if payload.code is not None:
                continent.code = payload.code
            if payload.population is not None:
                continent.population = payload.population
            continent.update("system")
            self.session.commit()

            return continent
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, continent: ContinentModel) -> ContinentModel:
        """_summary_

        Args:
            continent (ContinentModel): _description_

        Raises:
            e: _description_

        Returns:
            ContinentModel: _description_
        """
        try:
            continent.delete("system")
            self.session.commit()

            return continent
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> Optional[ContinentModel]:
        """_summary_

        Args:
            id (int): _description_

        Raises:
            e: _description_

        Returns:
            Optional[ContinentModel]: _description_
        """
        try:
            continent = (
                self.session.query(ContinentModel)
                .filter(ContinentModel.id == id)
                .first()
            )

            return continent
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_code(self, code: str) -> Optional[ContinentModel]:
        """_summary_

        Args:
            code (str): _description_

        Raises:
            e: _description_

        Returns:
            ContinentModel: _description_
        """
        try:
            continent = (
                self.session.query(ContinentModel)
                .filter(ContinentModel.code == code)
                .first()
            )

            return continent
        except Exception as e:
            self.session.rollback()
            raise e

    def find_all(self) -> List[ContinentModel]:
        """_summary_

        Raises:
            e: _description_

        Returns:
            List[ContinentModel]: _description_
        """
        try:
            continents = self.session.query(ContinentModel).filter(ContinentModel.is_deleted == False).all()

            return continents
        except Exception as e:
            self.session.rollback()
            raise e

    def reactivate(self, continent: ContinentModel) -> ContinentModel:
        try:
            continent.reactivate("system")
            self.session.commit()
            return continent
        except Exception as e:
            self.session.rollback()
            raise e