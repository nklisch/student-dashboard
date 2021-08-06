from fastapi import APIRouter, status, Depends
from ..schemas.requests import RequestConfig
from ..schemas.requests import ClassCreate
from typing import List, Optional
from ..dependencies import get_semester, get_db, get_sprint
from sqlalchemy.orm import Session
from ..schemas.reports import StudentActivityReport
from ..actions.buildReports import get_student_activity_report
from ..schemas.db_schemas import Sprint, User

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.post(
    "/student_activity",
    response_model=StudentActivityReport,
    status_code=status.HTTP_200_OK,
)
def automatic_populate_repos(
    user: User, db: Session = Depends(get_db), sprint: Sprint = Depends(get_sprint)
):
    return get_student_activity_report(db=db, sprint=sprint, user=user)
