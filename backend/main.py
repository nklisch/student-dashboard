from fastapi import FastAPI
from models.Student import Student
app = FastAPI()


@app.get("/")
async def root():
    s = Student(name='Nathan', email='nklisch@gmail.com')
    return s.dict()
