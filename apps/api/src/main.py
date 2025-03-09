from fastapi import FastAPI
from pydantic import BaseModel
from src.app.router import router


class App:

    def __init__(self):
        self.__router = router
        self.__container = None

    @property
    def router(self):
        return self.__router

    @property
    def container(self):
        return self.__container

    def create(self) -> FastAPI:
        app = FastAPI("/api", openapi_url="/api/openapi.json")

        app.include_router(self.router)

        @app.get("/")
        async def root():
            return {"message": "Hello World"}

        return app

    def main():
        app = self.create_app()
        app.run()


if __name__ == "__main__":
    app = App()
    app.main()
