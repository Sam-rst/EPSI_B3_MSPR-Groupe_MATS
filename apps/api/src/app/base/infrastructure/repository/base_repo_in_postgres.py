from typing import List
from sqlalchemy.orm import Session
from src.app.base.domain.entity.base_entity import BaseEntity
from src.app.base.domain.interface.base_repository import BaseRepository
from src.app.base.infrastructure.model.base_model import BaseModel
from src.app.base.infrastructure.utils.base_mapping_utils import BaseMappingUtils


class BaseRepositoryInPostgres(BaseRepository):
    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, value: Session):
        self._session = value

    # def create(self, model: BaseModel) -> BaseEntity:
    #     """Create entity

    #     Args:
    #         entity (BaseEntity): _description_

    #     Returns:
    #         BaseEntity: _description_
    #     """
    #     model = BaseMappingUtils.model_to_entity(model)
    #     self.session.add(model)
    #     self.session.commit()
    #     return BaseMappingUtils.model_to_domain(model)

    # def update(self, entity: BaseEntity) -> BaseEntity:
    #     """Update entity

    #     Args:
    #         entity (BaseEntity): _description_

    #     Returns:
    #         BaseEntity: _description_
    #     """
    #     model = self._session.query(BaseModel).filter_by(id=entity.id).first()
    #     if model:
    #         updated_model = BaseMappingUtils.domain_to_model(entity)
    #         self._session.merge(updated_model)
    #         self._session.commit()
    #         return BaseMappingUtils.model_to_domain(updated_model)
    #     return None

    # def delete(self, entity: BaseEntity) -> BaseEntity:
    #     """Delete entity

    #     Args:
    #         entity (BaseEntity): _description_

    #     Returns:
    #         BaseEntity: _description_
    #     """
    #     model = self._session.query(BaseModel).filter_by(id=entity.id).first()
    #     if model:
    #         self._session.delete(model)
    #         self._session.commit()
    #         return entity
    #     return None

    # def find_by_id(self, id: int) -> BaseEntity:
    #     """Find entity by id

    #     Args:
    #         id (int): _description_

    #     Returns:
    #         BaseEntity: _description_
    #     """
    #     model = self._session.query(BaseModel).filter_by(id=id).first()
    #     if model:
    #         return BaseMappingUtils.model_to_domain(model)
    #     return None

    # def find_all(self) -> List[BaseEntity]:
    #     """Find all entities"""
    #     models = self._session.query(BaseModel).all()
    #     return [BaseMappingUtils.model_to_domain(model) for model in models]

    # def exists(self, id: int) -> bool:
    #     """Search if entity exists

    #     Args:
    #         id (int): _description_

    #     Returns:
    #         bool: _description_
    #     """
    #     return self._session.query(BaseModel).filter_by(id=id).count() > 0
