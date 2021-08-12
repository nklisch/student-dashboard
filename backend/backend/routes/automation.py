from fastapi import APIRouter, status, Depends
from ..schemas.db_schemas import Repo, Commit, Issue, Team, Pull, Metric, Sprint
from ..schemas.requests import RequestConfig
from ..schemas.requests import ClassCreate
from typing import List, Optional
from ..dependencies import get_semester, get_sprint, verify_user
from sqlalchemy.orm import Session
from ..globals import determine_semester

from ..processing.automation import (
    AutomateRepos,
    AutomateCommits,
    AutomateUserTeams,
    AutomateIssues,
    AutomatePulls,
)
from ..processing.metrics import calculate_metrics
from datetime import datetime

router = APIRouter(
    prefix="/automation", tags=["automation"], dependencies=[Depends(verify_user)]
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


@router.post(
    "/commits",
    response_model=Optional[List[Commit]],
    status_code=status.HTTP_201_CREATED,
)
def automatic_populate_commits(
    start_date: datetime,
    end_date: datetime,
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    semester = determine_semester(start_date)
    response = AutomateCommits(
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
    semester: str = Depends(get_semester),
    since: datetime = datetime.now(),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomateIssues(
        semester=semester, since=since, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response


@router.post(
    "/pulls", response_model=Optional[List[Pull]], status_code=status.HTTP_201_CREATED
)
def automatic_populate_issues(
    semester: str = Depends(get_semester),
    since: datetime = datetime.now(),
    request_config: Optional[RequestConfig] = RequestConfig(),
):
    response = AutomatePulls(
        semester=semester, since=since, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response


@router.post("/metrics", status_code=status.HTTP_201_CREATED)
def automatic_calculate_metrics(sprint: Sprint = Depends(get_sprint)):
    calculate_metrics(semester=sprint.semester, sprintId=sprint.id)
