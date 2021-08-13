from fastapi import APIRouter, status, Depends
from ..schemas.requests import RequestConfig
from ..schemas.requests import ClassCreate
from typing import List, Optional
from ..dependencies import get_semester, get_sprint, verify_user, VerifyRole
from sqlalchemy.orm import Session
from ..schemas.reports import StudentActivityReport
from ..processing.reports import get_student_activity_report
from ..schemas.db_schemas import Sprint, User

router = APIRouter(
    prefix="/reports", tags=["reports"], dependencies=[Depends(verify_user)]
)


@router.get(
    "/student_activity/{userId}",
    response_model=StudentActivityReport,
    status_code=status.HTTP_200_OK,
)
def automatic_populate_repos(
    userId: int, sprintId: int, semester: str = Depends(get_semester)
):
    return get_student_activity_report(
        sprintId=sprintId, semester=semester, userId=userId
    )
