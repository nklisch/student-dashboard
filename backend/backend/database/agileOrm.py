from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from .util import toString

SQLBase = declarative_base()


class Sprints(SQLBase):
    __tablename__ = "Sprints"
    id = Column(String(15), primary_key=True)
    number = Column(Integer)
    semester = Column(String(10), ForeignKey("Classes.semester"))
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)

    def __repr__(self):
        return toString(self)


class Issues(SQLBase):
    __tablename__ = "Issues"
    id = Column(Integer, primary_key=True)
    createdBy = Column(Integer)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    epicId = Column(Integer)
    state = Column(String(10), nullable=False)
    sprintId = Column(String(15), ForeignKey("Sprints.id"))
    story_points = Column(Integer)
    opened = Column(DateTime)
    closed = Column(DateTime)

    def __repr__(self):
        return toString(self)


class Epics(SQLBase):
    __tablename__ = "Epics"
    id = Column(Integer, primary_key=True)
    issueId = Column(Integer)
    repoId = Column(Integer)

    def __repr__(self):
        return toString(self)
