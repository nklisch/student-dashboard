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
from ..configuration import database_settings
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.sql import func


class Commits(SQLBase):
    __tablename__ = "Commits"
    id = Column(String(150), autoincrement=False, primary_key=True)
    repo_id = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    date = Column(DateTime, nullable=False)
    author_id = Column(Integer)
    author_name = Column(String(150))
    author_email = Column(String(200))
    sprint_id = Column(Integer)
    semester = Column(String(10))
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprint_id", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="commits")

    def __repr__(self):
        return toString(self)


class Pulls(SQLBase):
    __tablename__ = "Pulls"
    id = Column(Integer, autoincrement=False, primary_key=True)
    repo_id = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    additions = Column(Integer)
    deletions = Column(Integer)
    commits = Column(Integer)
    changed_files = Column(Integer)
    merged_at = Column(DateTime)
    merged_by = Column(Integer)
    opened_by = Column(Integer, nullable=False)
    assigned_to = Column(Integer)
    sprint_id = Column(Integer)
    semester = Column(String(10))
    created_at = Column(DateTime)
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprint_id", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="pulls")

    def __repr__(self):
        return toString(self)


class Repos(SQLBase):
    __tablename__ = "Repos"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"))
    fullname = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    team = relationship("Teams", back_populates="repo", uselist=False)
    pulls = relationship("Pulls", back_populates="repo")
    commits = relationship("Commits", back_populates="repo")
    issues = relationship("Issues", back_populates="repo")

    def __repr__(self):
        return toString(self)


class Users(SQLBase):
    __tablename__ = "Users"
    id = Column(Integer, autoincrement=False, primary_key=True)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    github_login = Column(String(250), nullable=False)
    email = Column(String(100))
    name = Column(String(250))
    role = Column(Enum(Roles))
    active = Column(Boolean)
    avatar_url = Column(String(150))
    team = relationship("Teams", back_populates="members")

    def __repr__(self):
        return toString(self)


class Students(SQLBase):
    __tablename__ = "Students"
    user_id = Column(
        Integer, ForeignKey("Users.id"), autoincrement=False, primary_key=True
    )
    semester = Column(String(10), ForeignKey("Classes.semester"))

    def __repr__(self):
        return toString(self)


class Authentications(SQLBase):
    __tablename__ = "Authentication"
    user_id = Column(
        Integer, ForeignKey("Users.id"), autoincrement=False, primary_key=True
    )
    token = Column(
        StringEncryptedType(
            String, database_settings.DB_ENCRYPT_KEY, AesGcmEngine, "pkcs7", length=350
        )
    )
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now())
    valid = Column(Boolean)

    def __repr__(self):
        return toString(self)


class Audits(SQLBase):
    __tablename__ = "Audit"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    request = Column(String(50))
    date = Column(DateTime, server_default=func.now())
    success = Column(Boolean)
    message = Column(String(250))
    ip = Column(String(25))

    def __repr__(self):
        return toString(self)


class Teams(SQLBase):
    __tablename__ = "Teams"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"), primary_key=True)
    name = Column(String(250))
    repo_id = Column(Integer, ForeignKey("Repos.id"), nullable=False)
    repo = relationship("Repos", back_populates="team", uselist=False)
    members = relationship("Users", back_populates="team")
    Class = relationship("Classes", back_populates="teams")

    def __repr__(self):
        return toString(self)


class Classes(SQLBase):
    __tablename__ = "Classes"
    semester = Column(String(10), autoincrement=False, primary_key=True)
    git_organization = Column(String(25), nullable=False)
    teams = relationship("Teams", back_populates="Class")
    sprints = relationship("Sprints", back_populates="Class")

    def __repr__(self):
        return toString(self)


# <---Agile--->
class Sprints(SQLBase):
    __tablename__ = "Sprints"
    id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), ForeignKey("Classes.semester"), primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    Class = relationship("Classes", back_populates="sprints")

    def __repr__(self):
        return toString(self)


class Issues(SQLBase):
    __tablename__ = "Issues"
    id = Column(Integer, autoincrement=False, primary_key=True)
    number = Column(Integer)
    created_by = Column(Integer)
    closed_by = Column(Integer)
    repo_id = Column(Integer, ForeignKey("Repos.id"), primary_key=True)
    epic_id = Column(Integer)
    state = Column(String(10), nullable=False)
    sprint_id = Column(Integer)
    semester = Column(String(10))
    pipeline = Column(String(25))
    story_points = Column(Integer)
    opened = Column(DateTime)
    closed = Column(DateTime)
    is_epic = Column(Boolean)
    __table_args__ = (
        ForeignKeyConstraint(
            ["sprint_id", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )
    repo = relationship("Repos", back_populates="issues")

    def __repr__(self):
        return toString(self)


class Metrics(SQLBase):
    __tablename__ = "Metrics"
    user_id = Column(Integer, autoincrement=False, primary_key=True)
    sprint_id = Column(Integer, autoincrement=False, primary_key=True)
    semester = Column(String(10), primary_key=True)
    commits = Column(Integer)
    pulls = Column(Integer)
    issues = Column(Integer)
    active_days = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["sprint_id", "semester"], ["Sprints.id", "Sprints.semester"]
        ),
    )

    def __repr__(self):
        return toString(self)
