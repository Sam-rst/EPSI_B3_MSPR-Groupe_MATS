from fastapi import FastAPI

from src.config.container import Container
from src.config.database import Database
from src.app.base.infrastructure.model.base_model import Base
from src.config.models import *


class Application:
    _app: FastAPI = None

    @staticmethod
    def get_app() -> FastAPI:
        if not Application._app:
            app = FastAPI(docs_url="/docs", openapi_url="/docs/openapi.json")
            app.include_router(Container.router)
            Application._app = app

            db = Database()
            Base.metadata.create_all(bind=db.engine)
        return Application._app


app = Application.get_app()
