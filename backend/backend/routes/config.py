from fastapi import APIRouter, status, Depends
from typing import List, Optional, Union, Tuple, Dict
from ..processing.config import setup_semester
from ..schemas.db_schemas import Sprint, Repo, Team, User, Class
from ..database.models import Users, Sprints, Classes, Students
from ..schemas.requests import RequestConfig
from sqlalchemy.orm import Session
from ..database import SQLBase
from ..dependencies import verify_user, VerifyRole, get_semester
from ..actions.actions import Action
from ..schemas.requests import Semester

requires_TeachingAssistant = VerifyRole("TeachingAssistant")
router = APIRouter(
    prefix="/config", tags=["setup"], dependencies=[Depends(requires_TeachingAssistant)]
)


@router.post("/repos", status_code=status.HTTP_201_CREATED)
def automatic_populate_repos(semester: str = Depends(get_semester)):
    AutomateRepos(semester=semester, request_config=request_config).populate()


@router.post("/teams", status_code=status.HTTP_201_CREATED)
def automatic_populate_teams(semester: str = Depends(get_semester)):
    AutomateUserTeams(semester=semester, request_config=request_config).populate()


@router.post("/semester", status_code=status.HTTP_201_CREATED)
def handle_setup_semester(new_semester: Semester):
    return setup_semester(
        semester=new_semester.semester,
        git_orginization=new_semester.git_organization,
        sprints=new_semester.sprints,
    )


@router.get("/semester")
def get_semester_setup(semester: str = Depends(get_semester)):
    return Action(model=Classes).get(filter_by={"semester": semester}, schema=Class)


@router.get("/semesters", response_model=List[Class])
def get_semesters():
    return Action(model=Classes).get_all(schema=Class)


@router.get("/users", response_model=List[User])
def get_users(semester: str = Depends(get_semester)):
    return Action(model=Users).get_all(
        filter_by={"semester": semester}, joins=[Students]
    )


@router.post("/user")
def create_or_update_user(user: User, status_code=status.HTTP_201_CREATED):
    Action(model=Users).create_or_update(user)
