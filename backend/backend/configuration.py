from pydantic import BaseSettings, HttpUrl, validator
from typing import Any, Dict, Optional
from .schemas.db_schemas import User, Class
import socket


class Settings(BaseSettings):
    production: Optional[bool]
    client_port: Optional[int]
    server_port: Optional[int]
    url_root: Optional[str]
    audits: Optional[bool]

    class Config:
        env_file = ".env"


class EnvironementSettings(BaseSettings):
    production: Optional[bool]
    client_port: Optional[int]
    server_port: Optional[int]
    url_root: Optional[HttpUrl]
    audits: Optional[bool]


def get_settings() -> Settings:

    settings = {
        "production": False,
        "server_port": 8000,
        "client_port": 3000,
        "url_root": "http://localhost",
        "audits": False,
    }
    settings.update(Settings().dict(exclude_unset=True))
    settings.update(EnvironementSettings().dict(exclude_unset=True))
    return Settings(**settings)


global_settings = get_settings()


class DatabaseSettings(BaseSettings):
    DB_DEV_URL: str
    DB_PROD_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ENCRYPT_KEY: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        url = values.get("DB_DEV_URL")
        DB_USER, DB_PASSWORD, DB_NAME = (
            values.get("DB_USER"),
            values.get("DB_PASSWORD"),
            values.get("DB_NAME"),
        )
        if socket.getfqdn() == "cs.colostate.edu":
            url = values.get("DB_PROD_URL")
        return f"mariadb+mariadbconnector://{DB_USER}:{DB_PASSWORD}@{url}/{DB_NAME}"

    class Config:
        case_sensitive = True
        env_file = ".env"


class GitHubSettings(BaseSettings):
    github_key: str
    zenhub_key: str
    github_client_id: str
    github_client_secret: str

    class Config:
        env_file = ".env"


database_settings = DatabaseSettings()
github_settings = GitHubSettings()
