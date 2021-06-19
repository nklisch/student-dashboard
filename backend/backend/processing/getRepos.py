from .gitconnection import github
from ..database.repo import Repos

# TODO: add a query to database for the orginization string
# TODO: add a semester query/function that generates it base on the current date
def generate_repos_inserts():
    repos = [
        repo
        for repo in github.get_organization("csucs314s21").get_repos()
        if repo.name[0] == "t"
    ]
    inserts = []
    for repo in repos:
        r = Repos(
            id=repo.id,
            semester="Spring2021",
            fullName=repo.full_name,
            repoUrl=repo.url,
        )
        inserts.append(r)

    return inserts
