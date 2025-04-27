from fastapi import HTTPException, status
from src.app.role.presentation.model.payload.create_role_payload import (
    CreateRolePayload,
)
from src.app.role.domain.interface.role_repository import RoleRepository
from src.app.base.application.usecase.base_usecase import BaseUseCase
from src.app.role.presentation.model.dto.bulk_insert_roles_response_dto import (
    BulkInsertRolesResponseDTO,
    BulkInsertRolesErrorItemDTO,
    BulkInsertRolesSuccessItemDTO,
)


class ImportRolesUseCase(BaseUseCase):
    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    def execute(
        self, payloads: list[CreateRolePayload]
    ) -> BulkInsertRolesResponseDTO:
        try:
            success = []
            errors = []
            for payload in payloads:
                existing_role = self.repository.find_by_name(payload.name)
                if existing_role:
                    if not existing_role.is_deleted:
                        # Si le role existe et n'est pas supprimé, on l'ajoute à la liste des erreurs
                        errors.append(
                            BulkInsertRolesErrorItemDTO(
                                name=payload.name,
                                error="Le nom du role existe déjà",
                            )
                        )
                    else:
                        # Si le role existe mais est supprimé, on le restaure
                        self.repository.reactivate(existing_role)
                        success.append(
                            BulkInsertRolesSuccessItemDTO(
                                name=payload.name,
                                status="reactivated",
                            )
                        )
                else:
                    # Si le role n'existe pas, on le crée
                    self.repository.create(payload)
                    success.append(
                        BulkInsertRolesSuccessItemDTO(
                            name=payload.name,
                            status="created",
                        )
                    )
            return BulkInsertRolesResponseDTO(
                success=success,
                errors=errors,
            )

        except HTTPException as http_exc:
            # On relance les erreurs HTTP explicites (404, 400, etc.)
            raise HTTPException(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue: {str(e)}",
            )
