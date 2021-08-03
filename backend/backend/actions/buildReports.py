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

# def get_user_commit_report():


# def build_users_commit_reports(db: Session, semester: str, sprint: Sprint):
#     f = {"semester": semester, "sprintId": sprint.id}
#     users = User.from_orm(
#         db.query(Users).filter_by(f.update({"role": "Student"})).all()
#     )
#     teams = Team.from_orm(db.query(Teams).filter_by(f)).all()
#     metrics = []
#     avgs = []
#     usersIndexes = []
#     studentIndex = None
#     for index, user in enumerate(users):
#         results = (
#             db.query(Commits.date, functions.count(Commits.authorId))
#             .filter_by(f.update({"authorId": user.id}))
#             .group_by(Commit.authorId)
#             .group_by(Commit.date)
#             .all()
#         )
#         metrics.append(
#             [
#                 Metric(number=result[2], date=result[1], activity="Commits")
#                 for result in results
#             ]
#         )
#         usersIndexes.append(
#             UserIndex(
#                 index=index,
#                 userId=user.id,
#                 name=user.name,
#                 email=user.email,
#                 githubLogin=user.githubLogin,
#             )
#         )
#         if user.id == autheticatedUser.id:
#             studentIndex = usersIndexes[-1]
#     return InstructorReport(
#         indexes=usersIndexes,
#         sprint=Sprint,
#         semester=semester,
#         data=metrics,
#     )
