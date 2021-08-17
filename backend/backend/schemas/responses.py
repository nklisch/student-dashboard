from . import Semester
from datetime import datetime, date, timedelta
from pydantic import BaseModel, HttpUrl, conint, EmailStr, Field
from typing import List, Optional
from ..globals import Roles
from .db_schemas import Sprint
from . import Semester


class SemesterOut(BaseModel):
    sprints: Optional[Sprint]
    semester: str = Semester
    gitOrganization: str
