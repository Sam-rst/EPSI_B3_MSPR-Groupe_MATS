from abc import ABC, abstractmethod
from typing import Dict, List

import pandas as pd

from src.app.base.presentation.model.payload.base_payload import FilterRequest


class MachineLearningRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check_label_in_table_statistic(self, label: str) -> bool:
        pass

    @abstractmethod
    def check_value_in_model_from_column(
        self, column: str, value: str, model: str
    ) -> bool:
        pass

    @abstractmethod
    def get_data(self, payload: FilterRequest) -> List[dict]:
        pass

    @abstractmethod
    def get_predictions(self, data: pd.DataFrame) -> Dict:
        pass