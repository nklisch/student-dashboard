from enum import Enum


class Roles(str, Enum):
    SuperUser = 'SuperUser'
    Instructor = 'Instructor'
    TeachingAssistant = 'TeachingAssistant'
    Student = 'Student'
