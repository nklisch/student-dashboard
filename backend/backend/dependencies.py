from .globals import determine_semester
from datetime import date, datetime
from typing import Optional
from fastapi import Query
from .database import SessionLocal
from .actions.actions import Action
from .schemas.db_schemas import Sprint, Authentication, User
from .database.models import Authentications, Sprints, Users
from sqlalchemy.orm import Session
from fastapi import Depends, Cookie, HTTPException
from .globals import Roles


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


def verify_user(user_id: str = Cookie(None), token: str = Cookie(None)):
    auth = Action(model=Authentications).get(
        filter_by={"user_id": user_id}, schema=Authentication
    )

    if not auth or auth.token != token or not auth.valid:
        raise HTTPException(status_code=401, detail="Invalid token for given user")
    if datetime.now().day - auth.updated.day > 30:
        Action(model=Authentications).create_or_update({"valid": False})
        raise HTTPException(
            status_code=401,
            detail="Your token has expired, please reauthenticate",
            headers={"Clear-Site-Data": "cookies"},
        )
    return Action(model=Users).get(filter_by={"id": user_id}, schema=User)


class VerifyRole:
    def __init__(self, role: str):
        self.role = role

    def __call__(self, user: User = Depends(verify_user)):
        if not self.has_permission(self.role, user.role):
            raise HTTPException(
                status_code=403, detail="You do not have permission for this resource"
            )
        return user

    def has_permission(self, requiredRole: str, currentRole: str):
        role_value_map = {
            "SuperUser": 0,
            "Instructor": 1,
            "TeachingAssistant": 2,
            "Student": 3,
        }
        return role_value_map[currentRole] <= role_value_map[requiredRole]
