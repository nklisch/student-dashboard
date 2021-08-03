from pydantic import BaseModel, EmailStr
from .db_schemas import Sprint
from .db_schemas import Semester
from datetime import date
from ..globals import Metrics


class Average(BaseModel):
    activity: Metrics
    mean: float
    median: float


class Metric(BaseModel):
    activity: Metrics
    date: date
    number: int


class UserIndex(BaseModel):
    index: int
    userId: int
    name: Optional[str]
    email: EmailStr
    githubLogin: str


class TeamIndex(BaseModel):
    index: int
    teamId: int
    name: Optional[str]


class BaseReport(BaseModel):
    sprint: Sprint
    semester: str = Semester
    avgs: List[Metric]
    data: List[List[Metric]]


class StudentReport(BaseReport):
    index: Union[UserIndex, TeamIndex]


class InstructorReport(BaseReport):
    indexes: Union[List[UserIndex], List[TeamIndex]]
