from pydantic import BaseModel, HttpUrl, Field
from typing import (List, Optional)
from users import Team, User
from datetime import datetime, date
from agile import Issue


class Commit(BaseModel):
    id: str = Field(None, title="The unique SHA string attach to the commit.")
    repo_id: int
    date: datetime
    author: User
    sprint: int


class Pull(BaseModel):
    id: int
    repo_id: int
    merged_at: datetime
    opened_by: User
    assigned_to: User
    sprint: int


class Repo(BaseModel):
    id: int
    semester: str = Field(None, regex=r'^(spring|fall)20[0-9][0-9]$')
    full_name: str
    team: Team
    repo_url: HttpUrl
    issues: List[Issue]
    commits: List[Commit]
    pulls: List[Pull]
