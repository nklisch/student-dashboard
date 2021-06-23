from . import Semester
from datetime import datetime, date, timedelta
from pydantic import BaseModel, HttpUrl, conint, EmailStr, Field
from typing import List, Optional
from ..globals import Roles
