from fastapi import FastAPI
from src.config.container import Container

from src.app.continent.container import ContinentContainer
from src.app.continent.presentation.router import continent_router


class Application:
    _app: FastAPI = None

    @staticmethod
    def get_app() -> FastAPI:
        if not Application._app:
            app = FastAPI(docs_url="/docs", openapi_url="/docs/openapi.json")
            app.include_router(Container.router)
            Application._app = app
        return Application._app


app = Application.get_app()
