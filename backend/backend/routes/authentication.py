from fastapi import APIRouter, status, Depends, Response
from ..dependencies import verify_user
from ..processing.authentication import verify_user_on_github

router = APIRouter(
    prefix="/authenticate",
    tags=["authentication"],
)


@router.get("/user", dependencies=[Depends(verify_user)])
def authenticate_user():
    return {"authenticated": True}


@router.post("/update")
def github_authentication(code: str, response: Response):
    userId, token = verify_user_on_github(code)
    response.set_cookie(key="userId", value=str(userId))
    response.set_cookie(key="token", value=token)
    return {"authenticated": True}
