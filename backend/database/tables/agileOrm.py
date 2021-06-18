from sqlalchemyConnect import SQLBase, toString
from sqlalchemy import Column, Integer, String, Date, DateTime
from users import Roles
from enum import Enum


class Sprints(SQLBase):
    ___tablename__ = 'Sprints'
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey="Class.semester", primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def __repr__(self):
        return toString(self)


class Issues(SQLBase):
    __table__ = 'Issues'
    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey="Users.id")
    repo_id = Column(Integer, primary_key=True, ForeignKey="Repo.id")
    epic_id = Column(Integer)
    state = Column(String, nullable=False)
    sprint_id = Column(Integer, ForeignKey="Sprints.id")
    semester = Column(String, ForeignKey="Class.semester", primary_key=True)
    story_points = Column(Integer)
    opened = Column(DateTime)
    closed = Column(DateTime)

    def __repr__(self):
        return toString(self)


class Epics(SQLBase):
    __table__ = 'Epics'
    id = Column(Integer, primary_key=True)
    issueId = Column(Integer, ForeignKey="Issues.semester")

    def __repr__(self):
        return toString(self)
