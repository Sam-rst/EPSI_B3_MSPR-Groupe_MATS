# schemas.py
from pydantic import BaseModel
from typing import Any, List, Optional, Union
from enum import Enum


class Operator(str, Enum):
    """
    Opérateurs de comparaison disponibles pour les filtres.
    
    Attributes:
        eq: Égal à (=)
        ne: Différent de (!=)
        lt: Inférieur à (<)
        lte: Inférieur ou égal à (<=)
        gt: Supérieur à (>)
        gte: Supérieur ou égal à (>=)
        like: Contient (LIKE en SQL)
        in_: Dans une liste de valeurs (IN en SQL)
        between: Entre deux valeurs (BETWEEN en SQL)
    """
    eq = "="
    ne = "!="
    lt = "<"
    lte = "<="
    gt = ">"
    gte = ">="
    like = "like"
    in_ = "in"
    between = "between"


class FilterItem(BaseModel):
    """
    Représente un filtre à appliquer sur les données.
    
    Attributes:
        column (str): Nom de la colonne sur laquelle appliquer le filtre
        label (Optional[str]): Label spécifique pour les statistiques
        operator (Operator): Opérateur de comparaison à utiliser
        value (Union[str, int, float, List[Any]]): Valeur(s) à comparer
        model (str): Nom du modèle sur lequel appliquer le filtre

    Examples:
        ```json
        {
            "column": "value",
            "label": "totalVaccination",
            "operator": ">",
            "value": 1000,
            "model": "Statistic"
        }
        ```
    """
    column: str
    label: Optional[str] = None
    operator: Operator
    value: Union[str, int, float, List[Any]]
    model: str


class SortOption(BaseModel):
    """
    Options de tri pour les données.
    
    Attributes:
        column (str): Nom de la colonne sur laquelle trier
        model (str): Nom du modèle contenant la colonne
        direction (str): Direction du tri ("asc" ou "desc")

    Examples:
        ```json
        {
            "column": "value",
            "model": "Statistic",
            "direction": "desc"
        }
        ```
    """
    column: str
    model: str
    direction: str = "asc"  # ou "desc"


class Pagination(BaseModel):
    """
    Options de pagination pour les résultats.
    
    Attributes:
        page (int): Numéro de la page (commence à 1)
        per_page (int): Nombre d'éléments par page

    Examples:
        ```json
        {
            "page": 1,
            "per_page": 20
        }
        ```
    """
    page: int = 1
    per_page: int = 20


class Column(BaseModel):
    """
    Définition d'une colonne à inclure dans les résultats.
    
    Attributes:
        column (str): Nom de la colonne à sélectionner
        label (str): Nom d'affichage de la colonne dans les résultats
        model (str): Nom du modèle contenant la colonne

    Examples:
        ```json
        {
            "column": "value",
            "label": "total_vaccinations",
            "model": "Statistic"
        }
        ```
    """
    column: str
    label: str
    model: str


class FilterRequest(BaseModel):
    """
    Payload principal pour les requêtes de filtrage et d'export de données.
    
    Ce payload permet de :
    1. Filtrer les données avec des conditions complexes
    2. Trier les résultats
    3. Paginer les résultats
    4. Sélectionner les colonnes spécifiques à exporter

    Attributes:
        filters (Optional[List[FilterItem]]): Liste des filtres à appliquer
        sort (Optional[SortOption]): Options de tri
        pagination (Optional[Pagination]): Options de pagination
        columns (Optional[List[Column]]): Liste des colonnes à sélectionner

    Examples:
        ```json
        {
            "filters": [
                {
                    "column": "value",
                    "label": "totalVaccination",
                    "operator": ">",
                    "value": 1000,
                    "model": "Statistic"
                }
            ],
            "sort": {
                "column": "value",
                "model": "Statistic",
                "direction": "desc"
            },
            "pagination": {
                "page": 1,
                "per_page": 20
            },
            "columns": [
                {
                    "column": "value",
                    "label": "total_vaccinations",
                    "model": "Statistic"
                },
                {
                    "column": "date",
                    "label": "date",
                    "model": "DailyWise"
                }
            ]
        }
        ```

    Notes:
        - Les dates sont automatiquement converties en nombre de jours depuis le 1er janvier 1970
        - Les valeurs textuelles sont converties en entiers via un hash MD5
        - Les valeurs numériques sont conservées telles quelles
        - Les valeurs NULL sont converties en 0
    """
    filters: Optional[List[FilterItem]] = [
        FilterItem(column="", label="", operator="=", value="", model="")
    ]
    sort: Optional[SortOption] = SortOption(column="", direction="", model="")
    pagination: Optional[Pagination] = Pagination(page=1, per_page=20)
    columns: Optional[List[Column]] = [Column(column="", label="", model="")]
