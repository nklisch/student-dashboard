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


@router.get(
    "/student_activity",
    response_model=StudentActivityReport,
    status_code=status.HTTP_200_OK,
)
def automatic_populate_repos(
    userId: int,
    sprintId: int,
    semester: str = Depends(get_semester),
    db: Session = Depends(get_db),
):
    return get_student_activity_report(
        db=db, sprintId=sprintId, semester=semester, userId=userId
    )
