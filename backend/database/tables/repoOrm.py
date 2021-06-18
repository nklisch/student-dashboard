from sqlalchemyConnect import SQLBase, toString
from sqlalchemy import Column, Integer, String, Date, DateTime


class Commits(SQLBase):
    ___tablename__ = 'Commits'
    id = Column(Integer, primary_key=True)
    repoId = Column(Integer, primary_key=True, ForeignKey="Repos.id")
    date = Column(DateTime, nullable=False)
    authorId = Column(Integer, nullable=False)
    sprintId = Column(Integer, ForeignKey="Sprints.id")
    semester = Column(String, ForeignKey="Sprints.semester")

    def __repr__(self):
        return toString(self)


class Pull(SQLBase):
    ___tablename___ = 'Pulls'
    id = Column(Integer, primary_key=True)
    repoId = Column(Integer, primary_key=True, ForeignKey="Repos.id")
    merged_at = Column(DateTime)
    opened_by = Column(Integer, nullable=False)
    assigned_to = Column(Integer)
    sprintId = Column(Integer, "Sprints.id")
    semester = Column(String, ForeignKey="Sprints.semester")


class Repos(SQLBase):
    __tablename__ = 'Repos'
    id = Column(Integer, primary_key=True)
    fullName = Column(String, nullable=False)
    repoUrl = Column(String, nullable=False)
    accessKey = Column(String)
