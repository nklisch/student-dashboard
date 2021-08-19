from .gitconnection import github, zh
from ..database.models import (
    Repos,
    Classes,
    Users,
    Teams,
    Commits,
    Sprints,
    Issues,
    Pulls,
)
from ..schemas.db_schemas import Repo, Team, User, Commit, Issue, Pull
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
        semester: str,
        get_data: Callable,
        request_config: RequestConfig,
    ):
        self.semester = semester
        self.semester_setup = self.__check_semester_setup()
        self.sprints = Action(Sprints).get_all(filter_by={"semester": semester})
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
        result = Action(model=Classes).get(filter_by={"semester": self.semester})
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The current Semester of {semester} and Orginization have not been setup.",
            )
        return result


# TODO: Replace next structers with a pydantic model for better typing and hints for other devs


class AutomateRepos(Automate[Repos, Repo]):
    def __init__(self, semester: str, request_config: RequestConfig):
        super().__init__(semester, self.get_data, request_config)

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
    def __init__(self, semester: str, request_config: RequestConfig):
        super().__init__(semester, self.get_data, request_config)

    def get_data(
        self,
    ) -> List[Tuple[List[SchemaType], Type[SchemaType], Type[ModelType]]]:
        users = []
        teams = []
        current_users = set()
        for repo, team_number in super().get_valid_team_repos():
            teams.append(
                Team(
                    id=team_number, semester=self.semester, repoId=repo.id, schema=Team
                )
            )
            users.extend(self.get_users(repo, team_number, current_users))
        return [(teams, Team, Teams), (users, User, Users)]

    def get_users(self, repo: Repo, team_number: int, current_users: set):
        for member in repo.get_collaborators():
            if member.id not in current_users:
                current_users.add(member.id)
                if self.is_student(member) or team_number == 99:
                    current_users.add(member.id)
                    yield User(
                        id=member.id,
                        name=member.name,
                        githubLogin=member.login,
                        teamId=teamNumber,
                        semester=self.semester,
                        email=member.email,
                        active=False,
                        avatarUrl=member.avatar_url,
                        role="Student"
                        if self.is_student(member)
                        else "TeachingAssistant",
                    )

    def is_student(self, member):
        return member.permissions.admin != True


class AutomateCommits(Automate[Commits, Commit]):
    def __init__(
        self,
        semester: str,
        start_date: datetime,
        end_date: datetime,
        request_config: RequestConfig,
    ):
        super().__init__(semester, self.get_data, request_config)
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
    def __init__(
        self,
        semester: str,
        since: datetime,
        request_config: RequestConfig,
    ):
        super().__init__(semester, self.get_data, request_config)
        self.since = since

    def get_data(self) -> List[Tuple[List[Issues], Type[Issue], Type[Issues]]]:
        issues = []
        for repo, _ in super().get_valid_team_repos():
            for issue in repo.get_issues(state="all", since=self.since):
                zen_issue = zh.get_issue_data(
                    repo_id=repo.id, issue_number=issue.number
                )
                sleep(0.65)
                issues.append(
                    Issue(
                        id=issue.id,
                        number=issue.number,
                        repo_id=repo.id,
                        story_points=zen_issue["estimate"]["value"]
                        if "estimate" in zen_issue
                        else None,
                        opened=issue.created_at,
                        closed=issue.closed_at,
                        state=issue.state,
                        sprint_id=determine_sprint(
                            self.sprints, issue.created_at.date()
                        ),
                        pipeline=zen_issue["pipelines"][-1]["name"]
                        if "pipelines" in zen_issue
                        else None,
                        created_by=issue.user.id,
                        closed_by=issue.closed_by,
                        semester=self.semester,
                        is_epic=zen_issue["is_epic"],
                    )
                )
        return [(issues, Issue, Issues)]


class AutomatePulls(Automate[Pulls, Pull]):
    def __init__(
        self,
        semester: str,
        since: datetime,
        request_config: RequestConfig,
    ):
        super().__init__(semester, self.get_data, request_config)
        self.since = since

    def get_data(self) -> List[Tuple[List[Pulls], Type[Pull], Type[Pulls]]]:
        pulls = []
        for repo, _ in super().get_valid_team_repos():
            for pull in repo.get_pulls(state="all", direction="desc"):
                if self.since < pull.created_at:
                    pulls.append(
                        Pull(
                            id=pull.id,
                            repo_id=repo.id,
                            additions=pull.additions,
                            deletions=pull.deletions,
                            commits=pull.commits,
                            changed_files=pull.changed_files,
                            sprint_id=determine_sprint(
                                self.sprints,
                                pull.merged_at.date()
                                if pull.merged_at
                                else pull.created_at.date(),
                            ),
                            semester=self.semester,
                            merged_at=pull.merged_at,
                            opened_by=pull.user.id,
                            created_at=pull.created_at,
                            merged_by=pull.merged_by.id if pull.merged_by else None,
                            assigned_to=pull.assignee.id if pull.assignee else None,
                        )
                    )
                else:
                    break
        return [(pulls, Pull, Pulls)]
