from fastapi import APIRouter, status, Depends, Response, status
from ..schemas.db_schemas import User
from ..dependencies import verify_user
from ..processing.authentication import verify_user_on_github
from ..configuration import global_settings

router = APIRouter(
    prefix="/authenticate",
    tags=["authentication"],
)
expire_in_30_days = 2592000


@router.get("/user", response_model=User)
def authenticate_user(user: User = Depends(verify_user)):
    return user


@router.post("/update")
def github_authentication(code: str, response: Response):
    user_id, token = verify_user_on_github(code)
    response.set_cookie(key="user_id", value=str(user_id), expires=expire_in_30_days)
    response.set_cookie(key="token", value=token, expires=expire_in_30_days)
    return {"authenticated": True}


@router.get("/update")
def github_authentication(code: str, response: Response):
    user_id, token = verify_user_on_github(code)
    response.set_cookie(key="user_id", value=str(user_id), expires=expire_in_30_days)
    response.set_cookie(key="token", value=token, expires=expire_in_30_days)
    response.headers[
        "Location"
    ] = f"{global_settings.url_root}:{global_settings.client_port}"
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    return {"authenticated": True}
