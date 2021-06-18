from sqlalchemyConnect import SQLBase, toString
from sqlalchemy import Column, Integer, String
from users import Roles
from enum import Enum


class Users(SQLBase):
    ___tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    github_login = Column(String, nullable=False)
    oauth = Column(String)
    role = Column(Enum(Roles))
    semester = Column(String, ForeignKey="Classes.semester")
    team_number = Column(Integer)

    def __repr__(self):
        return toString(self)


class Teams(SQLBase):
    __table__ = 'Teams'
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey="Classes.semester", primary_key=True)
    name = Column(String)
    repoId = Column(Integer, nullable=False, ForeignKey="Repos.id")

    def __repr__(self):
        return toString(self)


class Classes(SQLBase):
    __table__ = 'Classes'
    semester = Column(String, primary_key=True)
    instructor = Column(String, nullable=False)

    def __repr__(self):
        return toString(self)
