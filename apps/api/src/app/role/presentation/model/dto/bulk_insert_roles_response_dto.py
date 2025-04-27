from typing import List, Optional
from pydantic import BaseModel


class BulkInsertRolesSuccessItemDTO(BaseModel):
    name: str  # Code de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertRolesErrorItemDTO(BaseModel):
    name: Optional[str]  # Code de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertRolesResponseDTO(BaseModel):
    success: List[BulkInsertRolesSuccessItemDTO]
    errors: List[BulkInsertRolesErrorItemDTO]
