from fastapi import APIRouter
from .auth_middleware import CheckAuthMiddleware

unprotected_api = APIRouter(prefix="/api")
protected_api = APIRouter(prefix="/api", route_class=CheckAuthMiddleware)
