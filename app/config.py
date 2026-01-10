import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn, RedisDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class APIPrefix(BaseModel):
    prefix: str = "/api"


class RedisConfig(BaseModel):
    url: RedisDsn


class CookieConfig(BaseModel):
    name: str
    age: int


class BrokerConfig(BaseModel):
    url: AmqpDsn


class DatabaseConfig(BaseModel):
    url: PostgresDsn  # парсит url базы данных
    echo: bool = False  # логирование SQL-запросов
    echo_pool: bool = False  # логирование работы пула соединений
    pool_size: int = 50  # максимальное количество соединений в пуле
    max_overflow: int = (
        10  # допустимое количество "временных" соединений сверх pool_size
    )


class SMTPConfig(BaseModel):
    host: str
    port: int
    from_email: str


class S3Config(BaseModel):
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str
    max_size: int


class VerificationConfig(BaseModel):
    ttl: int
    attempts: int
    code_len: int


class JWTConfig(BaseModel):
    private: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algoritm: str
    ttl: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,  # True если нужно учитывать регистр переменной
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api: APIPrefix = APIPrefix()
    logging: LoggingConfig = LoggingConfig()
    verification: VerificationConfig
    smtp: SMTPConfig
    redis: RedisConfig
    broker: BrokerConfig
    cookie: CookieConfig
    db: DatabaseConfig
    s3: S3Config
    jwt: JWTConfig


settings = Settings()
