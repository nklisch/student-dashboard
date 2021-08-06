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
        pulls = Action(db=db, model=Pulls).get_all(
            filter_by={"opened_by": user.id, **f}
        )
        pulls_count = len(pulls)
        issues = Action(db=db, model=Issues).get_all(
            filter_by={"createdBy": user.id, **f}
        )
        issues_count = len(issues)
        active_days = determine_active_days(commits, pulls, issues)
        metrics.append(
            Metric(
                userId=user.id,
                sprintId=sprintId,
                commits=commit_count,
                pulls=pulls_count,
                issues=issues_count,
                activeDays=active_days,
                semester=semester,
            )
        )
    Action(db=db, model=Metrics).create_or_update_all(metrics)


def determine_active_days(
    commits: List[Commit], pulls: List[Pulls], issues: List[Issues]
):
    dates = {commit.date.date(): 1 for commit in commits}
    dates.update({issue.opened.date(): 1 for issue in issues})
    dates.update({pull.merged_at.date(): 1 for pull in pulls if pull.merged_at})
    return sum(dates.values())
