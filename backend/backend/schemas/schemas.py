from datetime import datetime, date
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import List, Optional
from ..globals import Roles


class User(BaseModel):
    id: int
    githubLogin: str
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    email: Optional[EmailStr]
    name: Optional[str]
    role: Optional[Roles]
    active: Optional[bool]


class Team(BaseModel):
    id: int
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    name: str
    members: List[User]
    repoId: int


class Class(BaseModel):
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    gitOrganization: str
    teams: Optional[List[Team]]
    instructor: Optional[User]
    teachingAssistants: Optional[List[User]]


class Sprint(BaseModel):
    number: int
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
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
    title: str
    issues: List[Issue]


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
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    fullName: str
    team: Optional[Team]
    url: HttpUrl
    accessKey: Optional[str]
    issues: Optional[List[Issue]]
    commits: Optional[List[Commit]]
    pulls: Optional[List[Pull]]

    class Config:
        orm_mode = True
