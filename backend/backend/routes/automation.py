from fastapi import APIRouter, status, Depends
from ..schemas.db_schemas import Repo, Commit, Issue, Team, Pull
from ..schemas.requests import RequestConfig
from ..schemas.requests import ClassCreate
from typing import List, Optional
from ..dependencies import get_semester, get_db
from sqlalchemy.orm import Session
from ..processing.automation import (
    AutomateRepos,
    AutomateCommits,
    AutomateUserTeams,
    AutomateIssues,
    AutomatePulls,
)
from datetime import datetime

router = APIRouter(
    prefix="/automation",
    tags=["automation"],
)


@router.post(
    "/repos", response_model=Optional[List[Repo]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_repos(
    db: Session = Depends(get_db),
    semester: str = Depends(get_semester),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateRepos(
        db=db, semester=semester, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response


@router.post(
    "/teams", response_model=Optional[List[Team]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_teams(
    db: Session = Depends(get_db),
    semester: str = Depends(get_semester),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateUserTeams(
        db=db, semester=semester, request_config=request_config
    ).populate()[0]
    if request_config.get_response_body:
        return response


@router.post(
    "/commits",
    response_model=Optional[List[Commit]],
    status_code=status.HTTP_201_CREATED,
)
def automatic_populate_commits(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    semester = determine_semester(start_date)
    response = AutomateCommits(
        db=db,
        semester=semester,
        start_date=start_date,
        end_date=end_date,
        request_config=request_config,
    ).populate()
    if request_config.get_response_body:
        return response


@router.post(
    "/issues", response_model=Optional[List[Issue]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_issues(
    db: Session = Depends(get_db),
    semester: str = Depends(get_semester),
    since: datetime = datetime.now(),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateIssues(
        db=db, semester=semester, since=since, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response


@router.post(
    "/pulls", response_model=Optional[List[Pull]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_issues(
    db: Session = Depends(get_db),
    semester: str = Depends(get_semester),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomatePulls(
        db=db, semester=semester, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response
