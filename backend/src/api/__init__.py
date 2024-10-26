from fastapi import APIRouter
from .tasks import router as tasks_router

main_router = APIRouter(prefix="/api")
main_router.include_router(tasks_router)