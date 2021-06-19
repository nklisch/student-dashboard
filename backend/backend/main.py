from fastapi import Depends, FastAPI, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from .database.usersOrm import SQLBase
from .db import SessionLocal, engine
from .models import *

app = FastAPI()

SQLBase.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    s = User(id=1, name="Nathan", email="nklisch@gmail.com", githubLogin="nklisch")
    return s.dict()
