from pydantic import BaseSettings, HttpUrl, PostgresDsn, validator
from typing import Any, Dict, Optional


class Settings(BaseSettings):
    production: Optional[bool]
    client_port: Optional[int]
    server_port: Optional[int]
    url_root: Optional[HttpUrl]

    class Config:
        env_file = ".env"


class EnvironementSettings(BaseSettings):
    production: Optional[bool]
    client_port: Optional[int]
    server_port: Optional[int]
    url_root: Optional[HttpUrl]


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_ENCRYPT_KEY: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or  ''}",
        )

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


def get_settings() -> Settings:
    settings = {
        "production": False,
        "server_port": 8000,
        "client_port": 3000,
        "url_root": "http://localhost",
    }
    settings.update(Settings().dict())
    settings.update(EnvironementSettings().dict())
    return Settings(**settings)


global_settings = get_settings()
database_settings = DatabaseSettings()
github_settings = GitHubSettings()
