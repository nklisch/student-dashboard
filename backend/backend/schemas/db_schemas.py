from pydantic import BaseModel
from typing import Optional
from . import Semester
from datetime import datetime, date, timedelta
from pydantic import BaseModel, HttpUrl, conint, EmailStr, Field
from typing import List, Optional
from ..globals import Roles


class User(BaseModel):
    id: int
    githubLogin: str
    semester: str = Semester
    teamId: Optional[int]
    email: Optional[EmailStr]
    name: Optional[str]
    role: Optional[Roles]
    active: Optional[bool]

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: int
    repoId: int
    semester: str = Semester
    name: Optional[str]
    members: Optional[List[User]]

    class Config:
        orm_mode = True


class Class(BaseModel):
    semester: str = Semester
    gitOrganization: str
    teams: Optional[List[Team]]
    instructor: Optional[User]
    teachingAssistants: Optional[List[User]]

    class Config:
        orm_mode = True


class Sprint(BaseModel):
    id: int
    semester: str = Semester
    startDate: date
    endDate: date

    class Config:
        orm_mode = True


class Issue(BaseModel):
    id: int
    number: int
    createdBy: int
    repoId: int
    isEpic: bool
    state: str
    sprintId: int
    semester: str = Semester
    sprint: Optional[Sprint]
    pipeline: Optional[str]
    opened: datetime
    epicId: Optional[int]
    storyPoints: Optional[int]
    closed: Optional[datetime]

    class Config:
        orm_mode = True


class Commit(BaseModel):
    id: str = Field(None, title="The unique SHA string attach to the commit.")
    repoId: int
    date: datetime
    semester: str
    sprintId: int
    authorId: Optional[int] = None
    sprint: Optional[Sprint]
    authorName: Optional[str]
    authorEmail: Optional[EmailStr]

    class Config:
        orm_mode = True


class Pull(BaseModel):
    id: int
    repoId: int
    additions: int
    deletions: int
    commits: int
    changed_files: int
    sprintId: int
    semester: str = Semester
    sprint: Sprint
    merged_at: datetime
    opened_by: User
    assigned_to: Optional[User]

    class Config:
        orm_mode = True


class Repo(BaseModel):
    id: int
    semester: str = Semester
    fullName: str
    url: HttpUrl
    team: Optional[Team]
    accessKey: Optional[str]
    issues: Optional[List[Issue]]
    commits: Optional[List[Commit]]
    pulls: Optional[List[Pull]]

    class Config:
        orm_mode = True
