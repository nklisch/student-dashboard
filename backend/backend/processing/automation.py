from .gitconnection import github
from ..database.models import Repos, Classes
from ..schemas import Repo
from sqlalchemy.orm import Session
from ..globals import determine_semester
from fastapi import HTTPException, status
from ..actions.actions import get_all, create_or_update_all

# TODO: check that repos are already in database first and/or catch error and move on
def populate_repos(db: Session, semester: str):
    result = db.query(Classes).filter(Classes.semester == semester).one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The current Semester of {semester} and Orginization have not been setup.",
        )
    repos = [
        create_repo_dict(repo, semester)
        for repo in github.get_organization(result.gitOrganization).get_repos()
        if isTeamRepo(repo)
    ]
    create_or_update_all(db, repos, Repos)
    # old_repos = get_repos(db=db, semester=semester)
    # if no_dup_repos(repos, old_repos):
    #     db.add_all()
    #     db.commit()
    #     return get_repos(db=db, semester=semester)
    return get_all(db, {"semester": semester}, Repos, Repo)


def isTeamRepo(repo):
    return repo.name[0] == "t" and len(repo.name) == 3


def create_repo_dict(repo, semester):
    return {
        "id": repo.id,
        "semester": semester,
        "fullName": repo.full_name,
        "url": repo.url,
    }


def no_dup_repos(repos, old_repos):
    return len(repos) != len(old_repos)
