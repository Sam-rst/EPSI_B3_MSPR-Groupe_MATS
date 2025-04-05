from typing import List
from sqlalchemy.orm import Session
from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.base.infrastructure.model.base_model import BaseModel


class BaseRepositoryInPostgres(BaseRepository):
    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, value: Session):
        self._session = value
