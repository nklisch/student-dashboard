from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..configuration import database_settings

SQLBase = declarative_base()
engine = create_engine(database_settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def toString(orm):
    # s = {
    #     attr: value
    #     for attr, value in orm.__dict__.iteritems()
    #     if not attr.startswith("__") and not callable(getattr(orm, attr))
    # }
    return f"{vars(orm)}"
