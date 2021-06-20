from ..database.models import Repos
from ..schemas import Repo
from sqlalchemy.orm import Session


def get_repos(db: Session, semester: str):
    result = db.query(Repos).filter(Repos.semester == semester).all()
    return [Repo.from_orm(repo) for repo in result]
