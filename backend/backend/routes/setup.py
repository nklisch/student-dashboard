from fastapi import APIRouter, status, Depends
from typing import List
from ..processing.setup import setup_semester
from ..schemas.db_schemas import Sprint
from ..schemas.requests import ClassCreate
from sqlalchemy.orm import Session
from ..database import SQLBase
from ..dependencies import verify_user

router = APIRouter(prefix="/setup", tags=["setup"], dependencies=[Depends(verify_user)])


@router.post("/semester", status_code=status.HTTP_201_CREATED)
def handle_setup_semester(newClass: ClassCreate, sprints: List[Sprint]):
    return setup_semester(newClass=newClass, sprints=sprints)
