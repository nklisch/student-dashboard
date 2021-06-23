from pydantic import BaseModel
from typing import Optional


class RequestConfig(BaseModel):
    get_response_body: Optional[bool] = False
    limit: Optional[int] = 100
    skip: Optional[int] = 0
