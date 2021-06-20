from fastapi import Depends, FastAPI, HTTPException, status, Query
from sqlalchemy.orm import Session
from .database import SQLBase, SessionLocal, engine
from .database.models import Classes
from typing import List, Optional
from .schemas import Class, Repo
from .processing.automation import populate_repos
from .globals import determine_semester

app = FastAPI()

SQLBase.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"hello": "world"}


@app.post(
    "/automate/repos", response_model=List[Repo], status_code=status.HTTP_201_CREATED
)
def automatic_populate_repos(
    semester: Optional[str] = Query(
        None,
        regex=r"^(spring|fall|summer)20[0-9][0-9]$",
        title="Populate Semester Repos",
        description="Populates the recieved semester's repositories.",
    ),
    db: Session = Depends(get_db),
):
    if not semester:
        semester = determine_semester()
    return populate_repos(db=db, semester=semester)
