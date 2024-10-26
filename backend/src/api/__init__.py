from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as task_router

main_router = APIRouter(prefix="/api")
main_router.include_router(task_router)
main_router.include_router(auth_router)
