from .repo import SQLBase
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum
from .util import toString
from ..globals import Roles


class Users(SQLBase):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    github_login = Column(String, nullable=False)
    oauth = Column(String(250))
    role = Column(Enum(Roles), nullable=False)
    semester = Column(String(10), ForeignKey("Classes.semester"))
    team_number = Column(Integer)

    def __repr__(self):
        return toString(self)


class Teams(SQLBase):
    __tablename__ = "Teams"
    id = Column(Integer, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"), primary_key=True)
    name = Column(String(250))
    repoId = Column(Integer, ForeignKey("Repos.id"), nullable=False)

    def __repr__(self):
        return toString(self)


class Classes(SQLBase):
    __tablename__ = "Classes"
    semester = Column(String(10), primary_key=True)
    instructor = Column(String(150), nullable=False)

    def __repr__(self):
        return toString(self)
