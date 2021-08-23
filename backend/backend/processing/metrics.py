from sqlalchemy.orm import Session
from ..schemas.db_schemas import Sprint
from ..database.models import Commits, Users, Pulls, Issues, Metrics, Students
from ..schemas.db_schemas import User, Team, Commit, Metric
from typing import List
from datetime import date
from ..actions.actions import Action


def calculate_metrics(semester: str, sprint_id: int):
    f = {"semester": semester}
    users = Action(model=Users).get_all(filter_by={**f}, schema=User, joins=[Students])
    metrics = []
    f["sprint_id"] = sprint_id
    for user in users:
        commits = Action(model=Commits).get_all(filter_by={"author_id": user.id, **f})
        commit_count = len(commits)
        pulls = Action(model=Pulls).get_all(filter_by={"opened_by": user.id, **f})
        pulls_count = len(pulls)
        issues = Action(model=Issues).get_all(filter_by={"created_by": user.id, **f})
        issues_count = len(issues)
        active_days = determine_active_days(commits, pulls, issues)
        metrics.append(
            Metric(
                user_id=user.id,
                sprint_id=sprint_id,
                commits=commit_count,
                pulls=pulls_count,
                issues=issues_count,
                active_days=active_days,
                semester=semester,
            )
        )
    Action(model=Metrics).create_or_update_all(metrics)


def determine_active_days(
    commits: List[Commit], pulls: List[Pulls], issues: List[Issues]
):
    dates = {commit.date.date(): 1 for commit in commits}
    dates.update({issue.opened.date(): 1 for issue in issues})
    dates.update({pull.merged_at.date(): 1 for pull in pulls if pull.merged_at})
    return sum(dates.values())
