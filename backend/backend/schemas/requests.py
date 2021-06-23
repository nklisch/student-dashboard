from pydantic import BaseModel
from typing import Optional
from . import Semester


class RequestConfig(BaseModel):
    get_response_body: Optional[bool] = False
    limit: Optional[int] = 100
    skip: Optional[int] = 0


class ClassCreate(BaseModel):
    semester: str = Semester
    gitOrganization: str
