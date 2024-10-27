import asyncio

import asyncpg
from alembic.config import Config as AlembicConfig
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from config import cfg, path_to_alembic_cfg
from loguru import logger


def init_db() -> None:
    async def create_db():
        db = await asyncpg.connect(
            host=cfg.postgresql.host,
            port=cfg.postgresql.port,
            user=cfg.postgresql.user,
            password=cfg.postgresql.password,
        )

        existing_databases = await db.fetch(
            "SELECT datname FROM pg_database WHERE datname = $1", cfg.postgresql.name
        )

        if not existing_databases:
            await db.execute(f'CREATE DATABASE "{cfg.postgresql.name}"')
            logger.success(f"Database '{cfg.postgresql.name}' created successfully.")
        else:
            logger.info(f"Database '{cfg.postgresql.name}' already exists.")

        await db.close()

    asyncio.run(create_db())

    config = AlembicConfig(path_to_alembic_cfg)
    script = ScriptDirectory.from_config(config)
    head_revision = script.get_current_head()

    with EnvironmentContext(
        config,
        script,
        fn=lambda rev, _: script._upgrade_revs(head_revision, rev),
        as_sql=False,
        revision_environment=True,
        directives={},
    ):
        script.run_env()
