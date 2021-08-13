from .gitconnection import settings
from github import Github
from fastapi import HTTPException
import requests
from ..actions.actions import Action
from ..schemas.db_schemas import User, Authentication
from ..database.models import Users, Authentications
from ..dependencies import get_semester
import secrets


def verify_user_on_github(code):
    try:
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            params={
                "code": code,
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
            },
            headers={"Accept": "application/json"},
        )
        if not response or "access_token" not in response.json():
            raise HTTPException(
                status_code=401, detail="Could not validate user with github"
            )
        github_token = response.json()["access_token"]
        user = Github(login_or_token=github_token).get_user()
        if user.total_private_repos == None:
            raise HTTPException(
                status_code=401, detail="Could not validate user with github"
            )
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Could not validate user with github"
        )
    user_token = secrets.token_urlsafe(64)
    Action(model=Users).create_or_update(
        {
            "id": user.id,
            "githubLogin": user.login,
            "email": user.email,
            "name": user.name,
            "active": True,
        }
    )
    Action(model=Authentications).create_or_update(
        Authentication(userId=user.id, token=user_token, valid=True)
    )
    return user.id, user_token
