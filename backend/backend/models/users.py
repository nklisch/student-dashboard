from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from ..globals import Roles


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
