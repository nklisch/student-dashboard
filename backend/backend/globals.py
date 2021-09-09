from enum import Enum
from datetime import date, datetime, timedelta


class Metrics(str, Enum):
    Commits = "Commits"
    Pulls = "Pulls"
    Issues = "Issues"
    ActiveDays = "ActiveDays"


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
    elif d.month == 8:
        if d.day >= 15:
            semester += "fall"
        else:
            semester += "summer"
    else:
        semester += "summer"
    return semester + d.strftime("%Y")


def determine_sprint(sprints, d: date) -> int:
    sprint = 0
    for s in sprints:
        if s.start_date <= d <= s.end_date:
            sprint = s.id
    if sprint == 0:
        minimum = date(5000, 1, 1) - d
        for s in sprints:
            if s.end_date - d < minimum:
                minimum = s.end_date - d
                sprint = s.id
    return sprint


def get_yesterday():
    return datetime.now() - timedelta(days=1)
