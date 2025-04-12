from typing import List, Optional
from pydantic import BaseModel


class BulkInsertEpidemicsSuccessItemDTO(BaseModel):
    name: str  # Code de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertEpidemicsErrorItemDTO(BaseModel):
    name: Optional[str]  # Code de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertEpidemicsResponseDTO(BaseModel):
    success: List[BulkInsertEpidemicsSuccessItemDTO]
    errors: List[BulkInsertEpidemicsErrorItemDTO]
