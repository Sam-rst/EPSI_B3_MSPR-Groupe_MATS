from fastapi import HTTPException, status
from src.app.vaccine.domain.entity.vaccine_entity import VaccineEntity
from src.app.vaccine.domain.interface.vaccine_repository import VaccineRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase


class FindVaccineByIdUseCase(BaseUseCase):
    def __init__(self, repository: VaccineRepository):
        super().__init__(repository)

    def execute(self, id: int) -> VaccineEntity:
        # Recherche le vaccin par son ID
        vaccine = self.repository.find_by_id(id)

        if not vaccine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le vaccin n'existe pas"
            )
        if vaccine.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le vaccin a été supprimé"
            )

        return vaccine