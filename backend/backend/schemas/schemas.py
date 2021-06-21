from datetime import datetime, date
from pydantic import BaseModel, HttpUrl, conint, EmailStr, Field
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

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: int
    repoId: int
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    name: Optional[str]
    members: Optional[List[User]]

    class Config:
        orm_mode = True


class ClassCreate(BaseModel):
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    gitOrganization: str


class Class(ClassCreate):
    teams: Optional[List[Team]]
    instructor: Optional[User]
    teachingAssistants: Optional[List[User]]

    class Config:
        orm_mode = True


class Sprint(BaseModel):
    id: int
    semester: str = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
    startDate: date
    endDate: date

    class Config:
        orm_mode = True


class Issue(BaseModel):
    id: int
    created_by: int
    repoId: int
    epicId: int
    state: str
    sprint: Sprint
    pipeline: str
    storyPoints: int
    opened: datetime
    closed: Optional[datetime]

    class Config:
        orm_mode = True


class Epic(Issue):
    title: str
    issues: List[Issue]

    class Config:
        orm_mode = True


class Commit(BaseModel):
    id: str = Field(None, title="The unique SHA string attach to the commit.")
    repoId: int
    date: datetime
    sprint: Sprint
    authorId: int
    authorName: Optional[str]
    authorEmail: Optional[EmailStr]

    class Config:
        orm_mode = True


class Pull(BaseModel):
    id: int
    repoId: int
    sprint: Sprint
    merged_at: datetime
    opened_by: User
    assigned_to: Optional[User]

    class Config:
        orm_mode = True


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
