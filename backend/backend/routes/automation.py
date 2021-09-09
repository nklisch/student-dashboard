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
from ..globals import get_yesterday

requires_TeachingAssistant = VerifyRole("TeachingAssistant")
router = APIRouter(
    prefix="/automation",
    tags=["automation"],
    dependencies=[Depends(requires_TeachingAssistant)],
)


@router.post("/commits", status_code=status.HTTP_201_CREATED)
def automatic_populate_commits(
    semester: str = Depends(get_semester),
    since: datetime = get_yesterday(),
    end_date: Optional[datetime] = datetime.now(),
):
    AutomateCommits(
        semester=semester, start_date=since, end_date=end_date
    ).populate()
   


@router.post("/issues", status_code=status.HTTP_201_CREATED)
def automatic_populate_issues(
    semester: str = Depends(get_semester), since: datetime = get_yesterday()
):
    AutomateIssues(semester=semester, since=since).populate()


@router.post("/pulls", status_code=status.HTTP_201_CREATED)
def automatic_populate_teams(
    semester: str = Depends(get_semester), since: datetime = get_yesterday()
):
    AutomatePulls(semester=semester, since=since).populate()


@router.post("/metrics", status_code=status.HTTP_201_CREATED)
def automatic_calculate_metrics(sprint: Optional[Sprint] = Depends(get_sprint)):
    calculate_metrics(semester=sprint.semester, sprint_id=sprint.id)
