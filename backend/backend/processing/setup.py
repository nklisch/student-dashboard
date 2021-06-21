from ..database.models import Repos, Classes, Users, Teams
from ..schemas import ClassCreate, Class
from sqlalchemy.orm import Session
from ..actions.actions import Action
from typing import Tuple, List


def setup_semester(db: Session, c: ClassCreate) -> ClassCreate:
    class_action = Action(db, model=Classes).create_or_update(c)
    return class_action.get({"semester": c.semester}, schema=Class)
