from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

SQLBase = declarative_base()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def toString(orm):
    s = {
        a: self[a]
        for a in dir(obj)
        if not a.startswith("__") and not callable(getattr(obj, a))
    }
    return f"{s}"
