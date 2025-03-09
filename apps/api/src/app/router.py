from fastapi import APIRouter
from src.app.health.router import health

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
# router.include_router(user.router, prefix="/user", tags=["user"])
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(projects.router, prefix="/projects", tags=["projects"])
# router.include_router(annotations.router, prefix="/annotations", tags=["annotations"])
# router.include_router(models.router, prefix="/models", tags=["models"])
# router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
# router.include_router(teams.router, prefix="/teams", tags=["teams"])
