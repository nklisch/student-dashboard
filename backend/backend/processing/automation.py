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
    Students,
)
from ..schemas.db_schemas import Repo, Team, User, Commit, Issue, Pull, Student
from sqlalchemy.orm import Session
from ..globals import determine_semester, determine_sprint
from fastapi import HTTPException, status
from ..actions.actions import Action
from typing import Tuple, List, Generic, TypeVar, Type, Dict, Callable, Union
from datetime import datetime, date
from pydantic import BaseModel
from ..database import SQLBase
from time import sleep

ModelType = TypeVar("ModelType", bound=SQLBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Automate(Generic[ModelType, SchemaType]):
    def __init__(self, semester: str, get_data: Callable):
        self.semester = semester
        self.semester_setup = self.__check_semester_setup()
        self.sprints = Action(Sprints).get_all(filter_by={"semester": semester})
        self.get_data = get_data

    def populate(self):
        self.__create_or_update_data(self.get_data())
        

    def __create_or_update_data(
        self,
        data_schema_model: List[Tuple[List[SchemaType], Type[ModelType]]],
    ):
        for data, model in data_schema_model:
            Action(model=model).create_or_update_all(data)

    def get_valid_team_repos(self):
        for repo in github.get_organization(
            self.semester_setup.git_organization
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
                detail=f"The current Semester of {self.semester} and Orginization have not been setup.",
            )
        return result


class AutomateRepos(Automate[Repos, Repo]):
    def __init__(self, semester: str):
        super().__init__(semester, self.get_data)

    def get_data(self):
        repos = [
            Repo(
                id=repo.id,
                semester=self.semester,
                fullname=repo.full_name,
                url=repo.url,
            )
            for repo, _ in super().get_valid_team_repos()
        ]
        return [(repos, Repos)]


class AutomateUserTeams(Automate[ModelType, SchemaType]):
    def __init__(self, semester: str):
        super().__init__(semester, self.get_data)

    def get_data(
        self,
    ) -> List[Tuple[List[SchemaType], Type[SchemaType], Type[ModelType]]]:
        users = []
        students = []
        teams = []
        current_users = set()
        for repo, team_number in super().get_valid_team_repos():
            teams.append(
                Team(
                    id=team_number, semester=self.semester, repo_id=repo.id, schema=Team
                )
            )
            for user, student in self.get_users_students(
                repo, team_number, current_users
            ):
                users.append(user)
                if student:
                    students.append(student)
        return [
            (teams, Teams),
            (users, Users),
            (students, Students),
        ]

    def get_users_students(self, repo: Repo, team_number: int, current_users: set):
        for member in repo.get_collaborators():
            if member.id not in current_users:
                current_users.add(member.id)
                if self.is_student(member) or team_number == 99:
                    current_users.add(member.id)
                    yield User(
                        id=member.id,
                        name=member.name,
                        github_login=member.login,
                        team_id=team_number,
                        email=member.email,
                        active=False,
                        avatar_url=member.avatar_url,
                        role="Student"
                        if self.is_student(member)
                        else "TeachingAssistant",
                    ), Student(
                        user_id=member.id, semester=self.semester
                    ) if self.is_student(
                        member
                    ) else None

    def is_student(self, member):
        return member.permissions.admin != True


class AutomateCommits(Automate[Commits, Commit]):
    def __init__(self, semester: str, start_date: datetime, end_date: datetime):
        super().__init__(semester, self.get_data)
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
                        repo_id=repo.id,
                        date=commit.commit.author.date,
                        author_id=commit.author.id if commit.author else None,
                        author_name=commit.commit.author.name,
                        author_email=commit.commit.author.email,
                        sprint_id=determine_sprint(self.sprints, d),
                        semester=self.semester,
                    )
                )
        return [(commits, Commits)]


class AutomateIssues(Automate[Issues, Issue]):
    def __init__(self, semester: str, since: datetime):
        super().__init__(semester, self.get_data)
        self.since = since

    def get_data(self) -> List[Tuple[List[Issues], Type[Issue], Type[Issues]]]:
        issues = []
        for repo, _ in super().get_valid_team_repos():
            for issue in repo.get_issues(state="all", since=self.since):
                zen_issue = zh.get_issue_data(
                    repo_id=repo.id, issue_number=issue.number
                )
                sleep(0.65)
                pipeline = zen_issue["pipeline"]["name"] if "pipeline" in zen_issue else None
                if issue.state == 'closed':
                    pipeline = 'closed'
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
                        pipeline=pipeline,
                        created_by=issue.user.id,
                        closed_by=issue.closed_by,
                        semester=self.semester,
                        is_epic=zen_issue["is_epic"],
                    )
                )
        return [(issues, Issues)]


class AutomatePulls(Automate[Pulls, Pull]):
    def __init__(self, semester: str, since: datetime):
        super().__init__(semester, self.get_data)
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
        return [(pulls, Pulls)]
