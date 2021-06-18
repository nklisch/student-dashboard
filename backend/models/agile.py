from datetime import datetime, date
from users import Team, User
from pydantic import BaseModel, Field
from typing import (List, Optional)


class Sprint(BaseModel):
    id: int
    semester: str = Field(
        None, regex=r'^(spring|fall|summer)20[0-9][0-9]$')
    startDate: date
    endDate: date


class Issue(BaseModel):
    id: int
    created_by: User
    repoId: int
    epicId: int
    state: str
    sprint: Sprint
    pipeline: str
    storyPoints: int
    opened: datetime
    closed: Optional[datetime]


class Epic(Issue):
    id: int
    issues: List[Issue]
