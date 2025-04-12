from typing import List, Optional
from pydantic import BaseModel


class BulkInsertContinentsSuccessItemDTO(BaseModel):
    code: str  # Code de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertContinentsErrorItemDTO(BaseModel):
    code: Optional[str]  # Code de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertContinentsResponseDTO(BaseModel):
    success: List[BulkInsertContinentsSuccessItemDTO]
    errors: List[BulkInsertContinentsErrorItemDTO]
