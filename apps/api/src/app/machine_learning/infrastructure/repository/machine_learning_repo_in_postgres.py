from typing import List, Optional
from sqlalchemy.orm import Session

from src.config.database import db
from src.app.machine_learning.domain.interface.machine_learning_repository import MachineLearningRepository

class MachineLearningRepositoryInPostgres(MachineLearningRepository):
    def __init__(self):
        pass