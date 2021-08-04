# <---Users--->
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    ForeignKeyConstraint,
)
from sqlalchemy_utils.types.encrypted.encrypted_type import (
    AesGcmEngine,
    StringEncryptedType,
)
from .db import toString, SQLBase
from ..globals import Roles
from .config import settings
from sqlalchemy.orm import relationship


class Commits(SQLBase):
    __tablename__ = "Commits"
    id = Column(String(150), autoincrement=False, primary_key=True)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    date = Column(DateTime, nullable=False)
    authorId = Column(Integer)
    authorName = Column(String(150))
    authorEmail = Column(String(200))
    sprintId = Column(Integer)
    semester = Column(String(10))
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprintId", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="commits")

    def __repr__(self):
        return toString(self)


class Pulls(SQLBase):
    __tablename__ = "Pulls"
    id = Column(Integer, autoincrement=False, primary_key=True)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    additions = Column(Integer)
    deletions = Column(Integer)
    commits = Column(Integer)
    changed_files = Column(Integer)
    merged_at = Column(DateTime)
    merged_by = Column(Integer)
    opened_by = Column(Integer, nullable=False)
    assigned_to = Column(Integer)
    sprintId = Column(Integer)
    semester = Column(String(10))
    created_at = Column(DateTime)
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprintId", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="pulls")


class Repos(SQLBase):
    __tablename__ = "Repos"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"))
    fullName = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    accessKey = Column(String(250))
    team = relationship("Teams", back_populates="repo", uselist=False)
    pulls = relationship("Pulls", back_populates="repo")
    commits = relationship("Commits", back_populates="repo")
    issues = relationship("Issues", back_populates="repo")


# <---Users--->
class Users(SQLBase):
    __tablename__ = "Users"
    id = Column(Integer, autoincrement=False, primary_key=True)
    teamId = Column(Integer)
    semester = Column(String(10))
    githubLogin = Column(String(250), nullable=False)
    email = Column(String(100))
    name = Column(String(250))
    oauth = Column(
        StringEncryptedType(String, settings.DB_ENCRYPT_KEY, AesGcmEngine, "pkcs7")
    )
    role = Column(Enum(Roles))
    active = Column(Boolean)
    team = relationship("Teams", back_populates="members")
    __table_args__ = (
        ForeignKeyConstraint(["teamId", "semester"], ["Teams.id", "Teams.semester"]),
    )

    def __repr__(self):
        return toString(self)


class Teams(SQLBase):
    __tablename__ = "Teams"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"), primary_key=True)
    name = Column(String(250))
    repoId = Column(Integer, ForeignKey("Repos.id"), nullable=False)
    repo = relationship("Repos", back_populates="team", uselist=False)
    members = relationship("Users", back_populates="team")
    Class = relationship("Classes", back_populates="teams")

    def __repr__(self):
        return toString(self)


class Classes(SQLBase):
    __tablename__ = "Classes"
    semester = Column(String(10), autoincrement=False, primary_key=True)
    gitOrganization = Column(String(25), nullable=False)
    teams = relationship("Teams", back_populates="Class")

    def __repr__(self):
        return toString(self)


# <---Agile--->
class Sprints(SQLBase):
    __tablename__ = "Sprints"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"), primary_key=True)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)

    def __repr__(self):
        return toString(self)


class Issues(SQLBase):
    __tablename__ = "Issues"
    id = Column(Integer, autoincrement=False, primary_key=True)
    number = Column(Integer)
    createdBy = Column(Integer)
    closedBy = Column(Integer)
    repoId = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    epicId = Column(Integer)
    state = Column(String(10), nullable=False)
    sprintId = Column(Integer)
    semester = Column(String(10))
    pipeline = Column(String(25))
    storyPoints = Column(Integer)
    opened = Column(DateTime)
    closed = Column(DateTime)
    isEpic = Column(Boolean)
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprintId", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="issues")

    def __repr__(self):
        return toString(self)


class Metrics(SQLBase):
    __tablename__ = "Metrics"
    userId = Column(Integer, autoincrement=False, primary_key=True)
    sprintId = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), primary_key=True)
    commits = Column(Integer)
    pulls = Column(Integer)
    issues = Column(Integer)
    activeDays = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["sprintId", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )

    def __repr__(self):
        return toString(self)
