from typing import List, Optional
from pydantic import BaseModel


class BulkInsertCountriesSuccessItemDTO(BaseModel):
    iso3: str  # Iso3 de l'entité
    status: str  # Exemple: "created" | "reactivated"


class BulkInsertCountriesErrorItemDTO(BaseModel):
    iso3: Optional[str]  # Iso3 de l'entité si dispo
    error: str  # Message d'erreur métier


class BulkInsertCountriesResponseDTO(BaseModel):
    success: List[BulkInsertCountriesSuccessItemDTO]
    errors: List[BulkInsertCountriesErrorItemDTO]
