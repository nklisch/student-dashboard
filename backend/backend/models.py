from datetime import datetime, date
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import List, Optional
from enum import Enum


class Roles(str, Enum):
    SuperUser = "SuperUser"
    Instructor = "Instructor"
    TeachingAssistant = "TeachingAssistant"
    Student = "Student"


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    githubLogin: str
    oauth: Optional[str]
    role: Optional[Roles]
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")


class Team(BaseModel):
    id: int
    name: str
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    members: List[User]
    repoId: Optional[int]


class Class(BaseModel):
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    teams: List[Team]
    teachingAssistents: List[User]
    instructor: User


class Sprint(BaseModel):
    id: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]-[0-9]$")
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
    id: int
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
    team: Team
    repoUrl: HttpUrl
    accessKey: str
    issues: List[Issue]
    commits: List[Commit]
    pulls: List[Pull]
