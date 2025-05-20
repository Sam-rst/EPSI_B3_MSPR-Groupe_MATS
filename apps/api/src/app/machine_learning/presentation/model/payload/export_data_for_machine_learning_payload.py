from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class ExportDataForMachineLearningPayload(BaseModel):
    data: str