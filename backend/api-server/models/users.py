from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional, FrozenSet
from globals import Roles
from repo import Repo


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    githubLogin: str
    oauth: Optional[str]
    role: Optional[Roles]
    semester: Optional[date] = Field(
        None, regex=r'^(spring|fall|summer)20[0-9][0-9]$')
    team: Optional[Team]


class Team(BaseModel):
    id: int
    name: str
    semester: str = Field(
        None, regex=r'^(spring|fall|summer)20[0-9][0-9]$')
    repos: Repo
    members: List[User]


class Class(BaseModel):
    semester: str = Field(
        None, regex=r'^(spring|fall|summer)20[0-9][0-9]$')
    teams: List[Team]
    teachingAssistents: List[User]
    instructor: User
