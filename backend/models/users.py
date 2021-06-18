from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional, FrozenSet
from enum import Enum


class Roles(str, Enum):
    SuperUser = 'SuperUser'
    Instructor = 'Instructor'
    TeachingAssistant = 'TeachingAssistant'
    Student = 'Student'


class User(BaseModel):
    name: str
    github_login: str
    email: EmailStr
    oauth: Optional[str]
    role: Optional[Roles]
    semester: Optional[date]
    team: Optional[Team]


class Team(BaseModel):
    name: str
    number: int
    repo: str
    members: List[User]


class Class(BaseModel):
    semester: str = Field(regex=r'^(spring|fall)20[0-9][0-9]$')
    teams: List[Team]
    teaching_assistents: List[User]
