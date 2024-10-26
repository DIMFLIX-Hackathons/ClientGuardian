from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from utils.oauth2_utils import OAuth2Utils
from .sqladmin_auth import AdminAuth
from .sqladmin_views import all_views


def create_admin_panel(
    app: FastAPI,
    db_engine: AsyncEngine,
    jwt_secret_key: str,
    oauth_utils: OAuth2Utils,
    admin_login: str,
    admin_password: str,
) -> None:
    admin = Admin(
        app,
        db_engine,
        authentication_backend=AdminAuth(
            jwt_secret_key, oauth_utils, admin_login, admin_password
        ),
    )  # Admin panel

    for view in all_views:
        admin.add_view(view)  # Adding db tables to admin panel
