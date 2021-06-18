from pydantic import BaseModel, HttpUrl
from typing import (List, Optional)
from users import Team, User
from datetime import datetime, date


class Repo(BaseModel):
    id: int
    full_name: str
    team: Team
    repo_url: HttpUrl


class Issue(BaseModel):
    id: int
    state: str
    opened: datetime
    closed: Optional[datetime]
    sprint: int
    semester: str
    repo: HttpUrl
    storypoints: int
