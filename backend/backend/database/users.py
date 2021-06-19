from .repo import SQLBase
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum
from sqlalchemy_utils.types.encrypted.encrypted_type import (
    AesGcmEngine,
    StringEncryptedType,
)
from .util import toString
from ..globals import Roles
from .config import settings


class Users(SQLBase):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    github_login = Column(String(250), nullable=False)
    email = Column(String(100))
    fullName = Column(String(250))
    oauth = Column(
        StringEncryptedType(String, settings.DB_ENCRYPT_KEY, AesGcmEngine, "pkcs7")
    )
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
    gitorganization = Column(String(25), nullable=False)

    def __repr__(self):
        return toString(self)
