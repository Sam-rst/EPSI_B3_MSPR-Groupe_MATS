from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from src.config.container import Container
from src.config.database import Database
from src.app.base.infrastructure.model.base_model import Base
from src.config.models import *

from src.core.middlewares.limiter import limiter


class Application:
    _app: FastAPI = None

    @staticmethod
    def get_app() -> FastAPI:
        if not Application._app:
            app = FastAPI(docs_url="/docs", openapi_url="/docs/openapi.json")

            # Inintialisation des routers
            app.include_router(Container.router)

            # Initialisation des rates limits
            app.state.limiter = limiter
            app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
            Application._app = app

            Database()
        return Application._app


app = Application.get_app()
