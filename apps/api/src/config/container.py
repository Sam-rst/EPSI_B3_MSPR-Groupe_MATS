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


class Container(containers.DeclarativeContainer):
    containers = [
        ContinentContainer,
        CountryContainer,
        VaccineContainer,
        EpidemicContainer,
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
    router.include_router(continent_router, prefix="/continents")
    router.include_router(country_router, prefix="/countries")
    router.include_router(vaccine_router, prefix="/vaccines")
    router.include_router(epidemic_router, prefix="/epidemics")
