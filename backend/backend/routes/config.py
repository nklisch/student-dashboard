from fastapi import APIRouter, status, Depends
from typing import List, Optional
from ..processing.config import setup_semester
from ..schemas.db_schemas import Sprint, Repo, Team, User
from ..database.models import Users
from ..schemas.requests import ClassCreate, RequestConfig
from sqlalchemy.orm import Session
from ..database import SQLBase
from ..dependencies import verify_user, VerifyRole, get_semester
from ..actions.actions import Action

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
    response = AutomateRepos(emester=semester, request_config=request_config).populate()

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
def handle_setup_semester(newClass: ClassCreate, sprints: List[Sprint]):
    return setup_semester(newClass=newClass, sprints=sprints)


requires_Instructor = VerifyRole("Instructor")


@router.get(
    "/users", response_model=List[User], dependencies=[Depends(requires_Instructor)]
)
def get_users(semester: str = Depends(get_semester)):
    return Action(model=Users).get_all(filter_by={"semester": semester})


@router.post("/user", dependencies=[Depends(requires_Instructor)])
def create_or_update_user(user: User, status_code=status.HTTP_201_CREATED):
    Action(model=Users).create_or_update(user)
