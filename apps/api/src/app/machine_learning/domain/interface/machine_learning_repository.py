from abc import ABC, abstractmethod
from typing import List

from src.app.base.domain.interface.base_repository import BaseRepository


class MachineLearningRepository(BaseRepository, ABC):
    @abstractmethod
    def __init__(self):
        pass