from fastapi import APIRouter, status, Depends
from typing import List, Optional
from ..processing.setup import setup_semester
from ..schemas.db_schemas import Sprint, Repo, Team
from ..schemas.requests import ClassCreate, RequestConfig
from sqlalchemy.orm import Session
from ..database import SQLBase
from ..dependencies import verify_user, VerifyRole, get_semester

requires_TeachingAssistant = VerifyRole("TeachingAssistant")
router = APIRouter(
    prefix="/setup", tags=["setup"], dependencies=[Depends(requires_TeachingAssistant)]
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
