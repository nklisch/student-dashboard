from sqlalchemy.orm import Session
from ..schemas.db_schemas import Sprint
from ..database.models import Commits, Users, Metrics
from ..schemas.reports import StudentActivityReport, StudentMetric
from ..schemas.db_schemas import User, Team, Commit, Metric
from sqlalchemy.sql import functions
from ..actions.actions import Action
import pandas as pd
from scipy import stats


def get_student_activity_report(db: Session, sprint: Sprint, user: User):
    metrics = pd.DataFrame(
        [
            Metric.from_orm(row).dict()
            for row in Action(db=db, model=Metrics).get_all(
                filter_by={"semester": sprint.semester, "sprintId": sprint.id}
            )
        ]
    )
    score = Action(db=db, model=Metrics).get(
        filter_by={
            "semester": sprint.semester,
            "sprintId": sprint.id,
            "userId": user.id,
        }
    )

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
    return StudentActivityReport(
        user=user,
        issues=issues,
        pulls=pulls,
        commits=commits,
        active_days=active_days,
        sprint=sprint,
    )
