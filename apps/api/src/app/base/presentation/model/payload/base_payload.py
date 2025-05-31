# schemas.py
from pydantic import BaseModel
from typing import Any, List, Optional, Union
from enum import Enum


class Operator(str, Enum):
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
    column: str
    label: Optional[str] = None
    operator: Operator
    value: Union[str, int, float, List[Any]]
    model: str


class SortOption(BaseModel):
    column: str
    model: str
    direction: str = "asc"  # ou "desc"


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 20


class Column(BaseModel):
    column: str
    label: str
    model: str


class FilterRequest(BaseModel):
    filters: Optional[List[FilterItem]] = [
        FilterItem(column="", label="", operator="=", value="", model="")
    ]
    sort: Optional[SortOption] = SortOption(column="", direction="", model="")
    pagination: Optional[Pagination] = Pagination(page=1, per_page=20)
    columns: Optional[List[Column]] = [Column(column="", label="", model="")]
