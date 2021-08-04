from sqlalchemy.orm import Session
from ..schemas.db_schemas import Sprint
from ..database.models import Commits, Users
from ..schemas.db_schemas import User, Team, Commit
from sqlalchemy.sql import functions
from ..schemas.reports import (
    Average,
    Metric,
    UserIndex,
    TeamIndex,
    StudentReport,
    InstructorReport,
    BaseReport,
)

def get_user_commit_report():


def build_student_activity_report(db: Session, semester: str, sprint: Sprint):
    filter = {"semester": semester, "sprintId": sprint.id}
    users = User.from_orm(
        db.query(Users).filter_by(f.update({"role": "Student"})).all()
    )
    # need to filter by closed PRs here
   filter.update({"authorId": user.id}
    for user in users:
        commits = db.query(Commits)
            .filter_by()
            .group_by(Commits.authorId)
            .count()
        pulls = 

        issues =


        
    return 

