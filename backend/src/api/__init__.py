from fastapi import APIRouter
from .tasks import router as tasks_router
from .auth import router as auth_router

main_router = APIRouter(prefix="/api")
main_router.include_router(auth_router)
main_router.include_router(tasks_router)