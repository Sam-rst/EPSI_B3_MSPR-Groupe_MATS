from typing import List, Optional
from pydantic import BaseModel


class BulkInsertVaccinesSuccessItemDTO(BaseModel):
    name: str  # Nom de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertVaccinesErrorItemDTO(BaseModel):
    name: Optional[str]  # Nom de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertVaccinesResponseDTO(BaseModel):
    success: List[BulkInsertVaccinesSuccessItemDTO]
    errors: List[BulkInsertVaccinesErrorItemDTO]
