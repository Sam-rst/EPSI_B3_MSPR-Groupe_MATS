from abc import ABC, abstractmethod
from typing import List

from src.app.base.presentation.model.payload.base_payload import FilterRequest


class MachineLearningRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check_label_in_table_statistic(self, label: str) -> bool:
        pass

    @abstractmethod
    def get_data(self, payload: FilterRequest) -> List[dict]:
        pass
