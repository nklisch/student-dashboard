from pydantic import BaseModel, HttpUrl, Field
from typing import (List, Optional)
from users import Team, User
from datetime import datetime, date
from agile import Issue, Sprint


class Commit(BaseModel):
    id: str = Field(None, title="The unique SHA string attach to the commit.")
    repoId: int
    date: datetime
    author: User
    sprint: Sprint


class Pull(BaseModel):
    id: int
    repoId: int
    merged_at: datetime
    opened_by: User
    assigned_to: User
    sprint: Sprint


class Repo(BaseModel):
    id: int
    semester: str = Field(None, regex=r'^(spring|fall|summer)20[0-9][0-9]$')
    fullName: str
    team: Team
    repoUrl: HttpUrl
    accessKey: str
    issues: List[Issue]
    commits: List[Commit]
    pulls: List[Pull]
