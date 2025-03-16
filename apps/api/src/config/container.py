from dependency_injector import containers, providers
from fastapi import APIRouter

from src.app.continent.presentation.router import continent_router
from src.app.continent.container import ContinentContainer


class Container(containers.DeclarativeContainer):
    containers = [ContinentContainer]
    [container().wire(modules=container.modules) for container in containers]

    # A ajouter les autres routes si il y en a d'autres
    router = APIRouter()

    @router.get("/")
    def hello_world():
        return {"message": "Hello World"}

    @router.get("/health")
    def health():
        return {"message": "Application is running"}

    router.include_router(continent_router, prefix="/continents")
