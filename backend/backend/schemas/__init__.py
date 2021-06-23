from pydantic import Field

Semester = Field(None, regex=r"^(spring|fall|summer)20[0-9][0-9]$")
