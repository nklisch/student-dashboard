from .globals import determine_semester
from datetime import date
from typing import Optional
from fastapi import Query
from .database import SessionLocal


def get_semester(
    semester: Optional[str] = Query(
        determine_semester(date.today()),
        regex=r"^(spring|fall|summer)20[0-9][0-9]$",
        title="Populate Semester Repos",
        description="Populates the recieved semester's repositories.",
    )
) -> str:
    return semester


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
