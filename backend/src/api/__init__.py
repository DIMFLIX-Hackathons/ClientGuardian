from .tasks import router as task_router
from .auth import router as auth_router
from fastapi import APIRouter

main_router = APIRouter(prefix="/api")
main_router.include_router(task_router)
main_router.include_router(auth_router)