from fastapi import APIRouter, status, Depends, Response, status
from ..schemas.db_schemas import User
from ..dependencies import verify_user
from ..processing.authentication import verify_user_on_github

router = APIRouter(
    prefix="/authenticate",
    tags=["authentication"],
)


@router.get("/user", response_model=User)
def authenticate_user(user: User = Depends(verify_user)):
    return user


@router.post("/update")
def github_authentication(code: str, response: Response):
    userId, token = verify_user_on_github(code)
    response.set_cookie(key="userId", value=str(userId), expires=2592000)
    response.set_cookie(key="token", value=token, expires=2592000)
    return {"authenticated": True}


@router.get("/update")
def github_authentication(code: str, response: Response):
    userId, token = verify_user_on_github(code)
    response.set_cookie(key="userId", value=str(userId), expires=2592000)
    response.set_cookie(key="token", value=token, expires=2592000)
    response.headers["Location"] = "http://localhost:3000"
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    return {"authenticated": True}
