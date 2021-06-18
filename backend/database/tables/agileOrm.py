from sqlalchemyConnect import SQLBase, toString
from sqlalchemy import Column, Integer, String, Date, DateTime


class Sprints(SQLBase):
    ___tablename__ = 'Sprints'
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey="Classes.semester", primary_key=True)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)

    def __repr__(self):
        return toString(self)


class Issues(SQLBase):
    __table__ = 'Issues'
    id = Column(Integer, primary_key=True)
    createdBy = Column(Integer)
    repoId = Column(Integer, primary_key=True, ForeignKey="Repos.id")
    epicId = Column(Integer)
    state = Column(String, nullable=False)
    sprintId = Column(Integer, ForeignKey="Sprints.id")
    semester = Column(String, ForeignKey="Sprints.semester", primary_key=True)
    story_points = Column(Integer)
    opened = Column(DateTime)
    closed = Column(DateTime)

    def __repr__(self):
        return toString(self)


class Epics(SQLBase):
    __table__ = 'Epics'
    id = Column(Integer, primary_key=True)
    issueId = Column(Integer, ForeignKey="Issues.id")

    def __repr__(self):
        return toString(self)
