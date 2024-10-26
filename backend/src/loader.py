import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from admin import create_admin_panel
from config import cfg
from database.crud import CommonCRUD
from database.db_manager import DatabaseManager
from utils.oauth2_utils import OAuth2Utils

##==> Database
###################################################
db_manager = DatabaseManager(cfg.postgresql.url)
crud = CommonCRUD(db_manager)


##==> FastAPI
###################################################
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

oauth2: OAuth2Utils = OAuth2Utils(
    jwt_token_secret=cfg.jwt.secret_key,
    access_token_exp=cfg.jwt.access_token_exp,
    jwt_algorithm=cfg.jwt.algorithm,
)

create_admin_panel(
    app,
    db_engine=db_manager.engine,
    jwt_secret_key=cfg.jwt.secret_key,
    oauth_utils=oauth2,
    admin_login=cfg.admin.login,
    admin_password=cfg.admin.password,
)


##==> Logging
#################################################
logger.remove()

format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{module}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

logger.add(
    sink="logs/app.log",
    rotation=cfg.logs.rotation,
    retention=cfg.logs.retention,
    compression="zip",
    level=cfg.logs.level,
    format=format,
)

logger.add(sys.stderr, level=cfg.logs.level, format=format)
