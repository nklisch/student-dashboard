from pydantic import BaseSettings, PostgresDsn, validator
from github import Github
from zenhub import Zenhub


class Settings(BaseSettings):
    PRODUCTION: str
    GITHUB_KEY: str
    ZENHUB_KEY: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

github = Github(settings.GITHUB_KEY, per_page=100)
zh = Zenhub(settings.ZENHUB_KEY)
