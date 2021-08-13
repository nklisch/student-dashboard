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
        gh = Github(login_or_token=github_token)
        user = gh.get_user()
        user_email = None
        for email in user.get_emails():
            if email.primary:
                user_email = email.email
                break
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Could not validate user with github"
        )
    auth = Action(model=Authentications).get(
        filter_by={"userId": user.id}, schema=Authentication
    )
    user_token = auth.token if auth else None
    if not user_token or not auth.valid:
        user_token = secrets.token_urlsafe(64)
        try:
            Action(model=Users).create_or_update(
                {
                    "id": user.id,
                    "email": user_email,
                    "active": True,
                    "avatarUrl": user.avatar_url,
                }
            )
            Action(model=Authentications).create_or_update(
                Authentication(userId=user.id, token=user_token, valid=True)
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Could not add user to database: {e}"
            )
    return user.id, user_token
