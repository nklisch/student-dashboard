from fastapi import APIRouter, status, Depends
from typing import List, Optional, Union, Tuple, Dict
from ..processing.config import setup_semester
from ..schemas.db_schemas import Sprint, Repo, Team, User, Class
from ..database.models import Users, Sprints, Classes
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


@router.post(
    "/repos", response_model=Optional[List[Repo]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_repos(
    semester: str = Depends(get_semester),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateRepos(
        semester=semester, request_config=request_config
    ).populate()

    if request_config.get_response_body:
        return response


@router.post(
    "/teams", response_model=Optional[List[Team]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_teams(
    semester: str = Depends(get_semester),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateUserTeams(
        semester=semester, request_config=request_config
    ).populate()[0]
    if request_config.get_response_body:
        return response


@router.post("/semester", status_code=status.HTTP_201_CREATED)
def handle_setup_semester(new_semester: Semester):
    return setup_semester(
        semester=new_semester.semester,
        git_orginization=new_semester.git_organization,
        sprints=semester.sprints,
    )


@router.get("/semester", response_model=Semester)
def get_semester_setup(semester: str = Depends(get_semester)):
    sprints = Action(model=Sprints).get_all(
        filter_by={"semester": semester}, schema=Sprint
    )
    cl = Action(model=Classes).get(filter_by={"semester": semester}, schema=Class)
    git_organization = cl.git_organization if cl else None

    return Semester(
        sprints=sprints,
        git_organization=git_organization,
        semester=semester,
    )


requires_Instructor = VerifyRole("Instructor")


@router.get(
    "/users", response_model=List[User], dependencies=[Depends(requires_Instructor)]
)
def get_users(semester: str = Depends(get_semester)):
    return Action(model=Users).get_all(filter_by={"semester": semester})


@router.post("/user", dependencies=[Depends(requires_Instructor)])
def create_or_update_user(user: User, status_code=status.HTTP_201_CREATED):
    Action(model=Users).create_or_update(user)
