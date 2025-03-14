from fastapi import FastAPI
from src.app.router import router


class Application:
    _app: FastAPI = None

    @staticmethod
    def get_app() -> FastAPI:
        if not Application._app:
            app = FastAPI(
                docs_url="/api",
                openapi_url="/api/openapi.json"
            )
            app.include_router(router)
            Application._app = app
        return Application._app


app = Application.get_app()
