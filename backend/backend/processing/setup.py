from ..database.models import Repos, Classes, Users, Teams, Sprints
from ..schemas import ClassCreate, Class, Sprint
from sqlalchemy.orm import Session
from ..actions.actions import Action
from typing import Tuple, List


def setup_semester(db: Session, newClass: ClassCreate, sprints: List[Sprint]):
    class_action = Action(db, model=Classes).create_or_update(newClass)
    sprint_action = Action(db, model=Sprints).create_or_update_all(sprints)
