import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from src.config.container import Container
from src.config.database import Database
from src.app.base.infrastructure.model.base_model import Base
from src.config.models import *

from src.core.middlewares.limiter import limiter
from src.core.middlewares.security_headers import SecurityHeadersMiddleware
from src.core.config.settings import ENV, CORS_ORIGIN_WHITELIST

logger = logging.getLogger(__name__)


class Application:
    _app: FastAPI = None

    @staticmethod
    def get_app() -> FastAPI:
        if not Application._app:
            # Desactiver /docs et /redoc en production (fix C2 - exposition Swagger)
            is_prod = ENV and ENV.lower() == "production"
            app = FastAPI(
                docs_url=None if is_prod else "/docs",
                redoc_url=None if is_prod else "/redoc",
                openapi_url=None if is_prod else "/docs/openapi.json",
            )

            # Middleware security headers (fix C2 - CSP, HSTS, X-Frame-Options...)
            app.add_middleware(SecurityHeadersMiddleware)

            # CORS avec whitelist (fix C2 - CORS configure mais jamais applique)
            allowed_origins = []
            if CORS_ORIGIN_WHITELIST:
                allowed_origins = [
                    o.strip() for o in CORS_ORIGIN_WHITELIST.split(",")
                ]
            app.add_middleware(
                CORSMiddleware,
                allow_origins=allowed_origins,
                allow_credentials=True,
                allow_methods=["GET", "POST", "PUT", "DELETE"],
                allow_headers=["Authorization", "Content-Type"],
            )

            # Inintialisation des routers
            app.include_router(Container.router)

            # Initialisation des rates limits
            app.state.limiter = limiter
            app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

            # Handler d'erreur global : ne jamais exposer les stack traces (fix C2)
            @app.exception_handler(Exception)
            async def global_exception_handler(request: Request, exc: Exception):
                logger.error(f"Erreur interne: {exc}", exc_info=True)
                return JSONResponse(
                    status_code=500,
                    content={"message": "Une erreur interne est survenue."},
                )

            Application._app = app

            Database()
        return Application._app


app = Application.get_app()
