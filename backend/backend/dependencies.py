from .globals import determine_semester
from datetime import date, datetime
from typing import Optional
from fastapi import Query
from .database import SessionLocal
from .actions.actions import Action
from .schemas.db_schemas import Sprint, Authentication
from .database.models import Authentications, Sprints
from sqlalchemy.orm import Session
from fastapi import Depends, Cookie, HTTPException


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
    return SessionLocal()


def get_sprint(sprint: Optional[Sprint]) -> Sprint:
    if sprint:
        return sprint
    today = date.today()
    semester = determine_semester(today)
    sprints = Action(model=Sprints).get_all(
        filter_by={"semester": semester}, schema=Sprint
    )
    for sprint in sprints:
        if sprint.startDate <= today <= sprint.endDate:
            return sprint


def verify_user(userId: str = Cookie(None), token: str = Cookie(None)):
    auth = Action(model=Authentications).get(
        filter_by={"userId": userId}, schema=Authentication
    )

    if not auth or auth.token != token:
        raise HTTPException(status_code=401, detail="Invalid token for given user")
    if datetime.now().day - auth.updated.day > 30:
        Action(model=Authentications).create_or_update({"valid": False})
        raise HTTPException(
            status_code=401, detail="Your token has expired, please reauthenticate"
        )
