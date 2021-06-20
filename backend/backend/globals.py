from enum import Enum
from datetime import date


class Roles(str, Enum):
    SuperUser = "SuperUser"
    Instructor = "Instructor"
    TeachingAssistant = "TeachingAssistant"
    Student = "Student"


def determine_semester():
    today = date.today()
    semester = ""
    if 1 <= today.month <= 5:
        semester += "spring"
    elif 9 <= today.month <= 12:
        semester += "fall"
    else:
        semester += "summer"
    return semester + today.strftime("%Y")
