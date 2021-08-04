from pydantic import BaseModel, EmailStr
from .db_schemas import Sprint
from .db_schemas import Semester
from datetime import date
from ..globals import Metrics


class Metric(BaseModel):
    activity: Metrics
    score: int
    target: int


class InstructorMetric(Metric):
    mean: float
    median: float
    min: float
    max: float


class BaseReport(BaseModel):
    sprint: Sprint
    semester: str = Semester


class StudentActivity(BaseModel):
    issues: InstructorMetric
    pulls: InstructorMetric
    commits: InstructorMetric
    active_days: InstructorMetric


class StudentActivityReport(BaseReport):
    issues: Metric
    pulls: Metric
    commits: Metric
    active_days: Metric


class InstructorActivityReport(BaseReport):
    student_activities: List[StudentActivity]
