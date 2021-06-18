from datetime import datetime, date
from users import Team, User
from pydantic import BaseModel, Field
from typing import (List, Optional)


class Sprint(BaseModel):
    id: int
    semester: str = Field(
        None, regex=r'^(spring|fall)20[0-9][0-9]$')
    start_date: date
    end_date: date


class Issue(BaseModel):
    id: int
    created_by: User
    repo_id: int
    epic_id: int
    state: str
    sprint: Sprint
    pipeline: str
    story_points: int
    opened: datetime
    closed: Optional[datetime]


class Epic(Issue):
    id: int
    issues: List[Issue]
