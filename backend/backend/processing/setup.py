from ..database.models import Repos, Classes, Users, Teams, Sprints
from ..schemas.db_schemas import Class, Sprint
from ..schemas.requests import ClassCreate
from ..actions.actions import Action
from typing import Tuple, List


def setup_semester(newClass: ClassCreate, sprints: List[Sprint]):
    class_action = Action(model=Classes).create_or_update(newClass)
    sprint_action = Action(model=Sprints).create_or_update_all(sprints)
