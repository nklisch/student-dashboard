from fastapi import APIRouter, status, Depends
from typing import List
from ..processing.setup import setup_semester
from ..dependencies import get_db
from ..schemas import ClassCreate, Sprint
from sqlalchemy.orm import Session
from ..database import SQLBase

router = APIRouter(
    prefix="/setup",
    tags=["setup"],
)


@router.post("/semester", status_code=status.HTTP_201_CREATED)
def handle_setup_semester(
    newClass: ClassCreate, sprints: List[Sprint], db: Session = Depends(get_db)
):
    return setup_semester(db=db, newClass=newClass, sprints=sprints)
