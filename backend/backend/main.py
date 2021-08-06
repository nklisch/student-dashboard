from fastapi import Depends, FastAPI
from .routes import automation, setup, reports
from .database import SQLBase, engine

app = FastAPI()

SQLBase.metadata.create_all(bind=engine)
app.include_router(automation.router)
app.include_router(setup.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"hello": "world"}
