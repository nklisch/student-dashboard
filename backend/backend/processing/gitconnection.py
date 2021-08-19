from pydantic import BaseSettings, PostgresDsn, validator
from github import Github
from zenhub import Zenhub
from ..configuration import github_settings


github = Github(github_settings.github_key, per_page=100)
zh = Zenhub(github_settings.zenhub_key)
