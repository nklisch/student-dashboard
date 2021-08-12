from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import automation, setup, reports, authentication
from .database import SQLBase, engine
from .actions.actions import Action
from .database.models import Audits
from .schemas.db_schemas import AuditCreate
from sqlalchemy.orm import Session
from .dependencies import get_db
from starlette.responses import Response

app = FastAPI()

SQLBase.metadata.create_all(bind=engine)
app.include_router(automation.router)
app.include_router(setup.router)
app.include_router(reports.router)
app.include_router(authentication.router)


@app.get("/")
def root():
    return {"hello": "world"}


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def audit(request: Request, call_next):
    Action.db = get_db()
    request_url = request.base_url
    userId = request.cookies["userId"] if "userId" in request.cookies else None
    response = await call_next(request)
    Action(model=Audits).create(
        AuditCreate(
            userId=userId,
            request=request.base_url.path,
            ip=request.client.host,
            success=response.status_code < 300,
        )
    )
    Action.db.close()
    return response
