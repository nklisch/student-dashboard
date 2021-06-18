from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional, FrozenSet
from globals import Roles
from repo import Repo


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    github_login: str
    oauth: Optional[str]
    role: Optional[Roles]
    semester: Optional[date] = Field(
        None, regex=r'^(spring|fall)20[0-9][0-9]$')
    team: Optional[Team]


class Team(BaseModel):
    id: int
    name: str
    semester: str = Field(
        None, regex=r'^(spring|fall)20[0-9][0-9]$')
    repo: Repo
    members: List[User]


class Class(BaseModel):
    semester: str = Field(
        None, regex=r'^(spring|fall)20[0-9][0-9]$')
    teams: List[Team]
    teaching_assistents: List[User]
    instructor: User
