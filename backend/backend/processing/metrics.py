from sqlalchemy.orm import Session
from ..schemas.db_schemas import Sprint
from ..database.models import Commits, Users, Pulls, Issues, Metrics
from ..schemas.db_schemas import User, Team, Commit, Metric
from typing import List
from datetime import date
from ..actions.actions import Action


def calculate_metrics(db: Session, semester: str, sprintId: int):
    f = {"semester": semester}
    users = Action(db=db, model=Users).get_all(
        filter_by={"role": "Student", **f}, schema=User
    )
    metrics = []
    f["sprintId"] = sprintId
    for user in users:
        commits = Action(db=db, model=Commits).get_all(
            filter_by={"authorId": user.id, **f}
        )
        commit_count = len(commits)
        pulls = Action(db=db, model=Pulls).count(filter_by={"opened_by": user.id, **f})
        issues = Action(db=db, model=Issues).count(
            filter_by={"createdBy": user.id, **f}
        )
        active_days = determine_active_days(commits)
        metrics.append(
            Metric(
                userId=user.id,
                sprintId=sprintId,
                commits=commit_count,
                pulls=pulls,
                issues=issues,
                activeDays=active_days,
                semester=semester,
            )
        )
    Action(db=db, model=Metrics).create_or_update_all(metrics)


def determine_active_days(commits: List[Commit]):
    dates = {}
    for commit in commits:
        if commit.date.date() not in dates:
            dates[commit.date.date()] = 1
    return sum(dates.values())
