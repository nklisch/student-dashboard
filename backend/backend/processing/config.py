from ..database.models import Repos, Classes, Users, Teams, Sprints
from ..schemas.db_schemas import Class, Sprint
from ..actions.actions import Action
from typing import Tuple, List


def setup_semester(semester: str, git_orginization: str, sprints: List[Sprint]):
    class_action = Action(model=Classes).create_or_update(
        Class(semester=semester, git_organization=git_orginization)
    )
    sprint_action = Action(model=Sprints).create_or_update_all(sprints)
