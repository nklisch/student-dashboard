from .globals import determine_semester
from datetime import date
from typing import Optional
from fastapi import Query
from .database import SessionLocal
from .actions.actions import Action
from .schemas.db_schemas import Sprint
from sqlalchemy.orm import Session
from fastapi import Depends


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


def get_sprint(sprint: Optional[Sprint], db: Session = Depends(get_db)) -> Sprint:
    if sprint:
        return sprint
    today = date.today()
    semester = determine_semester(today)
    sprints = Action(db=db, model=Sprints).get_all(
        filter_by={"semester": semester}, schema=Sprint
    )
    for sprint in sprints:
        if sprint.startDate <= today <= sprint.endDate:
            return sprint
