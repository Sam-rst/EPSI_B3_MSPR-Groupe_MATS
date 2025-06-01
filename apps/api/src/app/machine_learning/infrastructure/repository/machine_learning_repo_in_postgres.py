from typing import List, Optional

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, between, func
from sqlalchemy.types import String, Text, DateTime, Date
import hashlib
from datetime import datetime

from src.config.database import db
from src.config.models import MODEL_REGISTRY
from src.app.machine_learning.domain.interface.machine_learning_repository import (
    MachineLearningRepository,
)
from src.app.base.presentation.model.payload.base_payload import FilterRequest

from src.app.statistic.infrastructure.model.statistic_model import StatisticModel
from src.app.daily_wise.infrastructure.model.daily_wise_model import DailyWiseModel
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.role.infrastructure.model.role_model import RoleModel


class MachineLearningRepositoryInPostgres(MachineLearningRepository):
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

    def check_label_in_table_statistic(self, label: str) -> bool:
        try:
            return (
                self.session.query(StatisticModel)
                .filter(StatisticModel.label == label)
                .first()
                is not None
            )
        except Exception as e:
            self.session.rollback()
            raise e

    def check_value_in_model_from_column(
        self, column: str, value: str, model: str
    ) -> bool:
        try:
            Model = MODEL_REGISTRY.get(model)
            if Model:
                column = getattr(Model, column, None)
                if column:
                    return (
                        self.session.query(column).filter(column == value).first()
                        is not None
                    )
        except Exception as e:
            self.session.rollback()
            raise e

    def get_data(self, payload: FilterRequest) -> List[dict]:
        """
        Récupère toutes les données nécessaires pour l'export CSV.
        À adapter selon votre modèle de données.
        """
        try:

            def get_filter_query(f, column, query):
                if f.operator == "in":
                    query = query.filter(column.in_(f.value))
                elif f.operator == "between":
                    query = query.filter(between(column, f.value[0], f.value[1]))
                else:
                    ops = {
                        "=": column == f.value,
                        "!=": column != f.value,
                        "<": column < f.value,
                        "<=": column <= f.value,
                        ">": column > f.value,
                        ">=": column >= f.value,
                        "like": column.like(f"%{f.value}%"),
                    }
                    query = query.filter(ops[f.operator])
                return query

            # Fonction pour hasher une valeur en entier
            def hash_to_int(value):
                if value is None:
                    return 0
                # Utiliser MD5 pour générer un hash, puis le convertir en entier
                hash_object = hashlib.md5(str(value).encode())
                # Prendre les 8 premiers caractères du hash et les convertir en entier
                return int(hash_object.hexdigest()[:8], 16)

            # Date de référence (1er janvier 1970)
            reference_date = datetime(1970, 1, 1)

            columns_selected = []
            for c in payload.columns:
                Model = MODEL_REGISTRY.get(c.model)
                if Model:
                    column = getattr(Model, c.column, None)
                    if column:
                        # Appliquer le hash pour les colonnes de type texte
                        if isinstance(column.type, (String, Text)):
                            column = func.abs(hash_to_int(column))
                        # Convertir les dates en nombre de jours depuis la date de référence
                        elif isinstance(column.type, (DateTime, Date)):
                            column = (
                                func.extract("epoch", column) / 86400
                            )  # Conversion en jours
                        columns_selected.append(column.label(c.label))

            query = (
                self.session.query(*columns_selected)
                .join(DailyWiseModel, StatisticModel.daily_wise_id == DailyWiseModel.id)
                .join(CountryModel, DailyWiseModel.country_id == CountryModel.id)
                .join(ContinentModel, CountryModel.continent_id == ContinentModel.id)
                .outerjoin(VaccineModel, StatisticModel.vaccine_id == VaccineModel.id)
                .outerjoin(
                    EpidemicModel, StatisticModel.epidemic_id == EpidemicModel.id
                )
            )

            # Appliquer les filtres de manière isolée
            for f in payload.filters:
                if f.label:
                    # Filtre sur le label
                    query = query.filter(StatisticModel.label == f.label)
                    # Filtre sur la valeur si spécifié
                    if hasattr(f, "value") and f.value is not None:
                        query = get_filter_query(f, StatisticModel.value, query)
                else:
                    # Filtre sur d'autres modèles
                    Model = MODEL_REGISTRY.get(f.model)
                    if Model:
                        column = getattr(Model, f.column, None)
                        if column:
                            query = get_filter_query(f, column, query)

            # Appliquer le tri
            if payload.sort:
                if payload.sort.column == "value":
                    order = (
                        asc(StatisticModel.value)
                        if payload.sort.direction == "asc"
                        else desc(StatisticModel.value)
                    )
                elif payload.sort.column == "label":
                    order = (
                        asc(StatisticModel.label)
                        if payload.sort.direction == "asc"
                        else desc(StatisticModel.label)
                    )
                else:
                    Model = MODEL_REGISTRY.get(payload.sort.model)
                    if Model:
                        column = getattr(Model, payload.sort.column, None)
                        if column:
                            order = (
                                asc(column)
                                if payload.sort.direction == "asc"
                                else desc(column)
                            )
                            query = query.order_by(order)
                query = query.order_by(order)

            # Appliquer la pagination
            offset = (payload.pagination.page - 1) * payload.pagination.per_page
            query = query.offset(offset).limit(payload.pagination.per_page)
            results = query.all()

            # Convertir les résultats en liste de dictionnaires
            return [dict(row._mapping) for row in results]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_predictions(self, data: pd.DataFrame) -> dict:
        """
        Obtenir les prédictions à partir des données fournies.

        Args:
            data (pd.DataFrame): Les données pour lesquelles obtenir des prédictions.

        Returns:
            dict: Les prédictions au format JSON.
        """
        try:
            # Ici, vous devez implémenter la logique pour obtenir les prédictions
            # en utilisant le modèle de machine learning approprié.
            # Pour l'instant, nous renvoyons un exemple de structure de données.
            predictions = {
                "predictions": data.to_dict(orient="records"),
                "message": "Prédictions générées avec succès."
            }
            return predictions
        except Exception as e:
            self.session.rollback()
            raise e