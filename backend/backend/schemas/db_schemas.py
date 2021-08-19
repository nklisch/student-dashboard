from pydantic import BaseModel
from typing import Optional
from . import Semester
from datetime import datetime, date, timedelta
from pydantic import BaseModel, HttpUrl, conint, EmailStr, Field
from typing import List, Optional
from ..globals import Roles


class AuditCreate(BaseModel):
    ip: str
    user_id: Optional[int]
    request: Optional[str]
    success: Optional[bool]
    message: Optional[str]

    class Config:
        orm_mode = True


class Authentication(BaseModel):
    user_id: int
    token: str
    created: Optional[datetime]
    updated: Optional[datetime]
    valid: bool

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    github_login: str
    semester: str = Semester
    team_id: Optional[int]
    email: Optional[EmailStr]
    name: Optional[str]
    role: Optional[Roles]
    active: Optional[bool]
    avatar_url: Optional[HttpUrl]

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: int
    repo_id: int
    semester: str = Semester
    name: Optional[str]
    members: Optional[List[User]]

    class Config:
        orm_mode = True


class Class(BaseModel):
    semester: str = Semester
    git_organization: str
    teams: Optional[List[Team]]
    instructor: Optional[User]
    teachingAssistants: Optional[List[User]]

    class Config:
        orm_mode = True


class Sprint(BaseModel):
    id: int
    semester: str = Semester
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        orm_mode = True


class Issue(BaseModel):
    id: int
    number: int
    created_by: int
    repo_id: int
    is_epic: bool
    state: str
    sprint_id: int
    semester: str = Semester
    sprint: Optional[Sprint]
    pipeline: Optional[str]
    opened: datetime
    epic_id: Optional[int]
    story_points: Optional[int]
    closed: Optional[datetime]

    class Config:
        orm_mode = True


class Commit(BaseModel):
    id: str = Field(None, title="The unique SHA string attach to the commit.")
    repo_id: int
    date: datetime
    semester: str
    sprint_id: int
    author_id: Optional[int] = None
    sprint: Optional[Sprint]
    authorName: Optional[str]
    authorEmail: Optional[EmailStr]

    class Config:
        orm_mode = True


class Pull(BaseModel):
    id: int
    repo_id: int
    additions: Optional[int]
    deletions: Optional[int]
    commits: Optional[int]
    changed_files: Optional[int]
    sprint_id: int
    semester: str = Semester
    merged_at: Optional[datetime]
    opened_by: int
    created_at: datetime
    merged_by: Optional[int]
    assigned_to: Optional[int]

    class Config:
        orm_mode = True


class Repo(BaseModel):
    id: int
    semester: str = Semester
    fullname: str
    url: HttpUrl
    team: Optional[Team]
    issues: Optional[List[Issue]]
    commits: Optional[List[Commit]]
    pulls: Optional[List[Pull]]

    class Config:
        orm_mode = True


class Metric(BaseModel):

    user_id: int
    sprint_id: int
    semester: str = Semester
    commits: int
    pulls: int
    issues: int
    active_days: int

    class Config:
        orm_mode = True
