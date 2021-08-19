from sqlalchemy.orm import Session
from ..schemas.db_schemas import Sprint
from ..database.models import Commits, Users, Metrics, Sprints
from ..schemas.reports import StudentActivityReport, StudentMetric
from ..schemas.db_schemas import User, Team, Commit, Metric
from sqlalchemy.sql import functions
from ..actions.actions import Action
import pandas as pd
from scipy import stats


def get_student_activity_report(sprint_id: int, semester: str, user_id: int):
    metrics = pd.DataFrame(
        [
            Metric.from_orm(row).dict()
            for row in Action(model=Metrics).get_all(
                filter_by={"semester": semester, "sprint_id": sprint_id}
            )
        ]
    )
    score = Action(model=Metrics).get(
        filter_by={
            "semester": semester,
            "sprint_id": sprint_id,
            "user_id": user_id,
        }
    )
    if not score:
        return None
    issues = StudentMetric(
        activity="Issues",
        score=score.issues,
        target=round(stats.trim_mean(metrics["issues"], proportiontocut=0.25)),
    )
    pulls = StudentMetric(
        activity="Pulls",
        score=score.pulls,
        target=round(stats.trim_mean(metrics["pulls"], proportiontocut=0.25)),
    )
    commits = StudentMetric(
        activity="Commits",
        score=score.commits,
        target=round(stats.trim_mean(metrics["commits"], proportiontocut=0.25)),
    )
    active_days = StudentMetric(
        activity="ActiveDays",
        score=score.activeDays,
        target=round(stats.trim_mean(metrics["activeDays"], proportiontocut=0.25)),
    )
    user = Action(model=Users).get(filter_by={"id": user_id}, schema=User)
    sprint = Action(model=Sprints).get(
        filter_by={"id": sprint_id, "semester": semester}, schema=Sprint
    )
    return StudentActivityReport(
        user=user,
        issues=issues,
        pulls=pulls,
        commits=commits,
        active_days=active_days,
        sprint=sprint,
    )
