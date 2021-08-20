from fastapi import APIRouter, status, Depends
from ..schemas.db_schemas import Repo, Commit, Issue, Team, Pull, Metric, Sprint
from ..schemas.requests import RequestConfig, Semester
from typing import List, Optional
from ..dependencies import get_semester, get_sprint, verify_user, VerifyRole
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

requires_TeachingAssistant = VerifyRole("TeachingAssistant")
router = APIRouter(
    prefix="/automation",
    tags=["automation"],
    dependencies=[Depends(requires_TeachingAssistant)],
)


@router.post(
    "/commits",
    status_code=status.HTTP_201_CREATED,
)
def automatic_populate_commits(start_date: datetime, end_date: datetime):
    semester = determine_semester(start_date)
    response = AutomateCommits(
        semester=semester,
        start_date=start_date,
        end_date=end_date,
        request_config=request_config,
    ).populate()
    if request_config.get_response_body:
        return response


@router.post("/issues", status_code=status.HTTP_201_CREATED)
def automatic_populate_issues(
    semester: str = Depends(get_semester), since: datetime = datetime.now()
):
    AutomateIssues(
        semester=semester, since=since, request_config=request_config
    ).populate()
    if request_config.get_response_body:
        return response


@router.post("/pulls", status_code=status.HTTP_201_CREATED)
def automatic_populate_issues(
    semester: str = Depends(get_semester), since: datetime = datetime.now()
):
    AutomatePulls(
        semester=semester, since=since, request_config=request_config
    ).populate()


@router.post("/metrics", status_code=status.HTTP_201_CREATED)
def automatic_calculate_metrics(sprint: Sprint = Depends(get_sprint)):
    calculate_metrics(semester=sprint.semester, sprint_id=sprint.id)
