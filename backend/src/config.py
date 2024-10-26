from pathlib import Path

from environs import Env
from pydantic import BaseModel

backend_src: Path = Path(__file__).resolve().parent
backend_root: Path = backend_src.parent
project_root: Path = backend_src.parent.parent
env_path = str(project_root / ".env")
path_to_alembic_cfg = str(backend_root / "alembic.ini")

env = Env()
env.read_env(env_path)


class PostgresConfig(BaseModel):
    host: str = env.str("DB_HOST", "localhost")
    port: int = env.int("DB_PORT", 5432)
    user: str = env.str("DB_USER", "postgres")
    password: str = env.str("DB_PASSWORD")
    name: str = env.str("DB_NAME", "ClientGuardian")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class JWTConfig(BaseModel):
    secret_key: str = env.str("JWT_SECRET_KEY")
    access_token_exp: int = env.int("JWT_ACCESS_TOKEN_EXP", 5)
    algorithm: str = env.str("JWT_ALGORITHM", "HS256")


class AdminAuthConfig(BaseModel):
    login: str = env.str("ADMIN_LOGIN")
    password: str = env.str("ADMIN_PASSWORD")


class LogsConfig(BaseModel):
    level: str = env.str("LOG_LEVEL", "INFO")
    retention: str = env.str("LOG_RETENTION", "7 days")
    rotation: str = env.str("LOG_ROTATION", "10 MB")


class ApiConfig(BaseModel):
    host: str = env.str("API_HOST")
    port: int = env.int("API_PORT", 5001)


class Config(BaseModel):
    postgresql: PostgresConfig = PostgresConfig()
    jwt: JWTConfig = JWTConfig()
    api: ApiConfig = ApiConfig()
    admin: AdminAuthConfig = AdminAuthConfig()
    logs: LogsConfig = LogsConfig()


cfg = Config()
