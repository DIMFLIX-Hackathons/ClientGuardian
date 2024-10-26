import asyncio
from argparse import ArgumentParser, RawTextHelpFormatter
from contextlib import asynccontextmanager
from database.init_db import init_db
from typing import AsyncGenerator

import uvicorn
from loguru import logger

from api import main_router as api_main_router
from config import cfg
from loader import app
from utils.loguru_integration import run_uvicorn_loguru


async def on_statup() -> None:
    logger.success(
        f"Панель администратора: http://{cfg.api.host}:{cfg.api.port}/admin"
    )


async def on_shutdown() -> None:
    ...


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator:
    await on_statup()

    try:
        yield
    finally:
        await on_shutdown()


def start() -> None:
    app.include_router(api_main_router)
    app.router.lifespan_context = lifespan

    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        logger.success("uvloop успешно установлен как стандартный цикл событий.")
    except ImportError:
        logger.info("uvloop не найден. Используется стандартный цикл событий asyncio.")

    try:
        run_uvicorn_loguru(
            uvicorn.Config(
                app,
                host=cfg.api.host,
                port=cfg.api.port,
                log_level=cfg.logs.level.lower(),
                reload=True,
            )
        )
    except KeyboardInterrupt:
        ...

if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('--init-db', help="Initialize database", action="store_true")
    args = parser.parse_args()
    logger.debug(f"Passed arguments: {args}")

    if args.init_db:
        init_db()
    else:
        start()