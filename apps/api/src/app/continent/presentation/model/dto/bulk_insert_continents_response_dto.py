from typing import List, Optional
from pydantic import BaseModel


class BulkInsertSuccessItemDTO(BaseModel):
    code: str  # Code de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertErrorItemDTO(BaseModel):
    code: Optional[str]  # Code de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertResponseDTO(BaseModel):
    success: List[BulkInsertSuccessItemDTO]
    errors: List[BulkInsertErrorItemDTO]
