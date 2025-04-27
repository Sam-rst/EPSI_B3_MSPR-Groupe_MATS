from dependency_injector import containers
from fastapi import APIRouter

from src.app.continent.container import ContinentContainer
from src.app.continent.presentation.router import continent_router
from src.app.country.container import CountryContainer
from src.app.country.presentation.router import country_router
from src.app.vaccine.container import VaccineContainer
from src.app.vaccine.presentation.router import vaccine_router
from src.app.epidemic.container import EpidemicContainer
from src.app.epidemic.presentation.router import epidemic_router
from src.app.user.container import UserContainer
from src.app.user.presentation.router import user_router
from src.app.role.container import RoleContainer
from src.app.role.presentation.router import role_router
from src.app.auth.container import AuthContainer
from src.app.auth.presentation.router import auth_router


class Container(containers.DeclarativeContainer):
    containers = [
        ContinentContainer,
        CountryContainer,
        VaccineContainer,
        EpidemicContainer,
        UserContainer,
        RoleContainer,
        AuthContainer,
    ]  # A ajouter les autres containers si il y en a d'autres
    [container().wire(modules=container.modules) for container in containers]

    router = APIRouter()

    @router.get("/")
    def hello_world():
        return {"message": "Hello World"}

    @router.get("/health")
    def health():
        return {"message": "Application is running"}

    # A ajouter les autres routes si il y en a d'autres
    router.include_router(continent_router, prefix="/continents", tags=["Continents"])
    router.include_router(country_router, prefix="/countries", tags=["Countries"])
    router.include_router(vaccine_router, prefix="/vaccines", tags=["Vaccines"])
    router.include_router(epidemic_router, prefix="/epidemics", tags=["Epidemics"])
    router.include_router(user_router, prefix="/users", tags=["Users"])
    router.include_router(role_router, prefix="/roles", tags=["Roles"])
    router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
