from .gitconnection import github, zh
from ..database.models import Repos, Classes, Users, Teams, Commits, Sprints, Issues
from ..schemas.db_schemas import Repo, Team, User, Commit, Issue
from sqlalchemy.orm import Session
from ..globals import determine_semester, determine_sprint
from fastapi import HTTPException, status
from ..actions.actions import Action
from typing import Tuple, List, Generic, TypeVar, Type, Dict, Callable, Union
from datetime import datetime, date
from pydantic import BaseModel
from ..database import SQLBase
from devtools import debug
from time import sleep
from ..schemas.requests import RequestConfig

ModelType = TypeVar("ModelType", bound=SQLBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Automate(Generic[ModelType, SchemaType]):
    def __init__(
        self,
        db: Session,
        semester: str,
        get_data: Callable,
        request_config: RequestConfig,
    ):
        self.db = db
        self.semester = semester
        self.semester_setup = self.__check_semester_setup()
        self.sprints = Action(db, Sprints).get_all(filter_by={"semester": semester})
        self.get_data = get_data
        self.request_config = request_config

    def populate(self) -> Union[List[List[SchemaType]], List[SchemaType]]:
        action_schemas = self.__create_or_update_data(self.get_data())
        if len(action_schemas) == 1:
            action, schema = action_schemas[0]
            return action.get_all(filter_by={"semester": self.semester}, schema=schema)

        return [
            action.get_all(
                filter_by={"semester": self.semester},
                schema=schema,
            )
            for action, schema in action_schemas
        ]

    def __create_or_update_data(
        self,
        data_schema_model: List[
            Tuple[List[SchemaType], Type[SchemaType], Type[ModelType]]
        ],
    ) -> List[Tuple[Action, Type[SchemaType]]]:
        return [
            (
                Action(
                    self.db,
                    model=model,
                    request_config=self.request_config,
                ).create_or_update_all(data),
                schema,
            )
            for data, schema, model in data_schema_model
        ]

    def get_valid_team_repos(self):
        for repo in github.get_organization(
            self.semester_setup.gitOrganization
        ).get_repos():
            if repo.name[0] == "t" and len(repo.name) == 3:
                try:
                    teamNumber = int(repo.name[1:])
                except ValueError:
                    break
                if teamNumber != 0:
                    yield repo, teamNumber

    def __check_semester_setup(self) -> Classes:
        result = Action(self.db, model=Classes).get(
            filter_by={"semester": self.semester}
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The current Semester of {semester} and Orginization have not been setup.",
            )
        return result


# TODO: Replace next structers with a pydantic model for better typing and hints for other devs


class AutomateRepos(Automate[Repos, Repo]):
    def __init__(self, db: Session, semester: str):
        super().__init__(db, semester, self.get_data)

    def get_data(self) -> List[Tuple[List[Repo], Type[Repo], Type[Repos]]]:
        repos = [
            Repo(
                id=repo.id,
                semester=self.semester,
                fullName=repo.full_name,
                url=repo.url,
            )
            for repo, _ in super().get_valid_team_repos()
        ]
        return [(repos, Repo, Repos)]


class AutomateUserTeams(Automate[ModelType, SchemaType]):
    def __init__(self, db: Session, semester: str):
        super().__init__(db, semester, self.get_data)

    def get_data(
        self,
    ) -> List[Tuple[List[SchemaType], Type[SchemaType], Type[ModelType]]]:
        users = []
        teams = []
        current_users = set()
        for repo, teamNumber in super().get_valid_team_repos():
            teams.append(
                Team(id=teamNumber, semester=self.semester, repoId=repo.id, schema=Team)
            )
            users.extend(self.get_users(repo, teamNumber, current_users))
        return [(teams, Team, Teams), (users, User, Users)]

    def get_users(self, repo: Repo, teamNumber: int, current_users: set):
        for member in repo.get_collaborators():
            if member.id not in current_users:
                current_users.add(member.id)
                if self.isStudent(member) or teamNumber == 99:
                    current_users.add(member.id)
                    yield User(
                        id=member.id,
                        name=member.name,
                        githubLogin=member.login,
                        teamId=teamNumber,
                        semester=self.semester,
                        email=member.email,
                        active=True,
                        role="Student" if self.isStudent(member) else None,
                    )

    def isStudent(self, member):
        return member.permissions.admin != True


class AutomateCommits(Automate[Commits, Commit]):
    def __init__(
        self, db: Session, semester: str, start_date: datetime, end_date: datetime
    ):
        super().__init__(db, semester, self.get_data)
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self) -> List[Tuple[List[Commit], Type[Commit], Type[Commits]]]:
        commits = []
        for repo, _ in super().get_valid_team_repos():
            for commit in repo.get_commits(since=self.start_date, until=self.end_date):
                d = commit.commit.author.date.date()
                commits.append(
                    Commit(
                        id=commit.sha,
                        repoId=repo.id,
                        date=commit.commit.author.date,
                        authorId=commit.author.id if commit.author else None,
                        authorName=commit.commit.author.name,
                        authorEmail=commit.commit.author.email,
                        sprintId=determine_sprint(self.sprints, d),
                        semester=self.semester,
                    )
                )
        return [(commits, Commit, Commits)]


class AutomateIssues(Automate[Issues, Issue]):
    def __init__(self, db: Session, semester: str, since: datetime):
        super().__init__(db, semester, self.get_data)
        self.since = datetime

    def get_data(self) -> List[Tuple[List[Issues], Type[Issue], Type[Issues]]]:
        issues = []
        for repo, _ in super().get_valid_team_repos():
            for issue in repo.get_issues(state="all"):
                zenIssue = zh.get_issue_data(repo_id=repo.id, issue_number=issue.number)
                sleep(0.65)
                issues.append(
                    Issue(
                        id=issue.id,
                        number=issue.number,
                        repoId=repo.id,
                        storyPoints=zenIssue["estimate"]["value"]
                        if "estimate" in zenIssue
                        else None,
                        opened=issue.created_at,
                        closed=issue.closed_at,
                        state=issue.state,
                        sprintId=determine_sprint(
                            self.sprints, issue.created_at.date()
                        ),
                        pipeline=zenIssue["pipelines"][-1]["name"]
                        if "pipelines" in zenIssue
                        else None,
                        createdBy=issue.user.id,
                        closedBy=issue.closed_by,
                        semester=self.semester,
                        isEpic=zenIssue["is_epic"],
                    )
                )
        return [(issues, Issue, Issues)]
