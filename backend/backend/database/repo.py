from .agile import SQLBase
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from .util import toString


class Commits(SQLBase):
    __tablename__ = "Commits"
    id = Column(Integer, primary_key=True)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    date = Column(DateTime, nullable=False)
    authorId = Column(Integer, nullable=False)
    sprintId = Column(String(15), ForeignKey("Sprints.id"))

    def __repr__(self):
        return toString(self)


class Pull(SQLBase):
    __tablename__ = "Pulls"
    id = Column(Integer, primary_key=True)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    merged_at = Column(DateTime)
    opened_by = Column(Integer, nullable=False)
    assigned_to = Column(Integer)
    sprintId = Column(String(15), ForeignKey("Sprints.id"))


class Repos(SQLBase):
    __tablename__ = "Repos"
    id = Column(Integer, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"))
    fullName = Column(String(50), nullable=False)
    repoUrl = Column(String(100), nullable=False)
    accessKey = Column(String(250))
