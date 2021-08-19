from pydantic import BaseModel
from typing import Optional, List
from .db_schemas import Sprint
from . import Semester as SemesterValidation


class RequestConfig(BaseModel):
    get_response_body: Optional[bool] = True
    limit: Optional[int] = 100
    skip: Optional[int] = 0


class Semester(BaseModel):
    sprints: Optional[List[Sprint]]
    semester: str = SemesterValidation
    git_organization: Optional[str]
