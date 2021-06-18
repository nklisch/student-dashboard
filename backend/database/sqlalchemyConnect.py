from sqlalchemy.orm import declarative_base

SQLBase = declarative_base()


def toString(orm):
    s = {a: self[a] for a in dir(obj) if not a.startswith(
        '__') and not callable(getattr(obj, a))}
    return f"{s}"
