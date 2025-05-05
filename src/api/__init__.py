"""Основной маршрутизатор объединяет несколько
дополнительных маршрутизаторов, связанных с
 различными функциональными возможностями приложения.
"""
from fastapi import APIRouter
from src.api.books import router as books_rourter_1
from src.api.users import router as users_router
from src.api.books_v2 import router as books_rourter_2
from src.api.utils import router as aurh_router
from src.api.optimization import router as opt_router


main_router = APIRouter()



main_router.include_router(books_rourter_1)
main_router.include_router(opt_router)
main_router.include_router(users_router)
main_router.include_router(books_rourter_2)
main_router.include_router(aurh_router)
