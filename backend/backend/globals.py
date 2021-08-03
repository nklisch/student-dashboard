from enum import Enum
from sqlalchemy.orm import Session
from datetime import date


class Metrics(str, Enum):
    Commits = "Commits"
    Pulls = "Pulls"
    Issues = "Issues"


class Roles(str, Enum):
    SuperUser = "SuperUser"
    Instructor = "Instructor"
    TeachingAssistant = "TeachingAssistant"
    Student = "Student"


def determine_semester(d):
    semester = ""
    if 1 <= d.month <= 5:
        semester += "spring"
    elif 9 <= d.month <= 12:
        semester += "fall"
    else:
        semester += "summer"
    return semester + d.strftime("%Y")


def determine_sprint(sprints, d: date) -> int:
    sprint = 0
    for s in sprints:
        if s.startDate <= d <= s.endDate:
            sprint = s.id
    if sprint == 0:
        minimum = date(5000, 1, 1) - d
        for s in sprints:
            if s.endDate - d < minimum:
                minimum = s.endDate - d
                sprint = s.id
    return sprint
