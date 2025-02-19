from pydantic import BaseModel, EmailStr
from .db_schemas import Sprint, User
from datetime import date
from ..globals import Metrics
from typing import List


class BaseMetric(BaseModel):
    activity: Metrics
    score: int


class StudentMetric(BaseMetric):
    target: int


class InstructorMetric(BaseMetric):
    mean: float
    median: float
    min: float
    max: float


class BaseReport(BaseModel):
    sprint: Sprint
    user: User


class StudentActivity(BaseModel):
    issues: InstructorMetric
    pulls: InstructorMetric
    commits: InstructorMetric
    active_days: InstructorMetric


class StudentActivityReport(BaseReport):
    issues: StudentMetric
    pulls: StudentMetric
    commits: StudentMetric
    active_days: StudentMetric


class InstructorActivityReport(BaseReport):
    student_activities: List[StudentActivity]
