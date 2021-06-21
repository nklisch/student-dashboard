from .gitconnection import github
from ..database.models import Repos, Classes, Users, Teams, Commits, Sprints
from ..schemas import Repo, Team
from sqlalchemy.orm import Session
from ..globals import determine_semester, determine_sprint
from fastapi import HTTPException, status
from ..actions.actions import Action
from typing import Tuple, List
from datetime import datetime, date

# <------------------Repos------------------>
def populate_repos(db: Session, semester: str):
    result = check_semester_setup(db, semester)
    repos = [
        create_repo_dict(repo, semester)
        for repo in github.get_organization(result.gitOrganization).get_repos()
        if isTeamRepo(repo)
    ]
    repo_action = Action(db, Repos).create_or_update_all(repos)
    return repo_action.get_all(filter_by={"semester": semester}, schema=Repo)


def isTeamRepo(repo):
    return repo.name[0] == "t" and len(repo.name) == 3


def create_repo_dict(repo, semester):
    return {
        "id": repo.id,
        "semester": semester,
        "fullName": repo.full_name,
        "url": repo.url,
    }


def check_semester_setup(db: Session, semester: str) -> Classes:
    result = Action(db, model=Classes).get(filter_by={"semester": semester})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The current Semester of {semester} and Orginization have not been setup.",
        )
    return result


# <----------------Users/Teams------------------->


def populate_users_and_teams(db: Session, semester: str) -> List[dict]:
    result = check_semester_setup(db, semester)
    users, teams = get_users_and_teams(semester, result.gitOrganization)
    teams_action = Action(db, Teams).create_or_update_all(teams)
    user_action = Action(db, Users).create_or_update_all(users)
    return teams_action.get_all(filter_by={"semester": semester})


def get_users_and_teams(semester: str, org: str) -> Tuple[List[dict]]:
    users = []
    teams = []
    current_users = set()
    for repo in github.get_organization(org).get_repos():
        if repo.name[0] == "t" and len(repo.name) == 3:
            teamNumber = int(repo.name[1:])
            if teamNumber != 0:
                teams.append(
                    {"id": teamNumber, "semester": semester, "repoId": repo.id}
                )
            for member in repo.get_collaborators():
                if member.id not in current_users:
                    if member.permissions.admin != True and teamNumber != 99:
                        users.append(
                            create_user_dict(
                                user=member,
                                semester=semester,
                                teamNumber=teamNumber,
                                active=True,
                            )
                        )
                        current_users.add(member.id)
                    elif teamNumber == 99:
                        users.append(
                            create_user_dict(
                                user=member,
                                semester=semester,
                                teamNumber=teamNumber,
                                active=True,
                            )
                        )
                        current_users.add(member.id)
    return users, teams


def create_user_dict(user, semester, teamNumber, active):
    return {
        "id": user.id,
        "name": user.name,
        "githubLogin": user.login,
        "teamId": teamNumber,
        "email": user.email,
        "semester": semester,
        "active": active,
    }


# <------Commits----->


def populate_commits(
    db: Session, semester: str, start_date: datetime, end_date: datetime
):
    result = check_semester_setup(db, semester)
    commits = get_commits(
        db=db,
        semester=semester,
        org=result.gitOrganization,
        start_date=start_date,
        end_date=end_date,
    )
    Action(db, Commits).create_or_update_all(commits)


def get_commits(
    db: Session, semester: str, org: str, start_date: datetime, end_date: datetime
) -> List[dict]:
    sprints = Action(db, Sprints).get_all(filter_by={"semester": semester})
    commits = []
    for repo in github.get_organization(org).get_repos():
        if repo.name[0] == "t" and len(repo.name) == 3:
            teamNumber = int(repo.name[1:])
            for commit in repo.get_commits(since=start_date, until=end_date):
                d = commit.commit.author.date.date()
                commits.append(
                    create_commit_dict(
                        commit, repo.id, determine_sprint(sprints, d), semester
                    )
                )
    return commits


def create_commit_dict(commit, repoId, sprintId, semester):
    return {
        "id": commit.sha,
        "repoId": repoId,
        "date": commit.commit.author.date,
        "authorId": commit.author.id if commit.author else 0,
        "authorName": commit.commit.author.name,
        "authorEmail": commit.commit.author.email,
        "sprintId": sprintId,
        "semester": semester,
    }
