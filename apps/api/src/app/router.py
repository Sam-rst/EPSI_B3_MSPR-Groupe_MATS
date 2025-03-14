from fastapi import APIRouter
from src.app.continent.presentation.router import continent_router

router = APIRouter()

# @router.get("")
# def hello_world():
#     return {"message": "Hello World"}

router.include_router(continent_router, tags=["continents"])