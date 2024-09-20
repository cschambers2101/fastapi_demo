from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlmodel import create_engine, Session, SQLModel, Field, select


class Students(SQLModel, table=True):
    ''' This class is used to create a table in the database for students'''
    __tablename__ = "students"
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str


class Student(SQLModel):
    ''' This class is used to create to map a response for a student'''
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str


# Setup the database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# Create the database and all tables
SQLModel.metadata.create_all(engine)

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware to the app
origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/students", response_model=Students)
async def create_student(student: Students):
    ''' This function is used to create a student in the database'''
    with Session(engine) as db:
        db.add(student)
        db.commit()
        db.refresh(student)
        return student


@app.get("/students", response_model=List[Students])
async def read_students():
    ''' This function is used to get all students in the database'''
    with Session(engine) as db:
        statement = select(Students)
        students = db.exec(statement).all()
        return students


@app.get("/students/{student_id}", response_model=Student)
async def read_student(student_id: int):
    ''' This function is used to get a student by id in the database'''
    with Session(engine) as db:
        statement = select(Students).where(Students.id == student_id)
        student = db.exec(statement).first()
        return student


@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: int):
    ''' This function is used to delete a student by id in the database'''
    with Session(engine) as db:
        statement = select(Students).where(Students.id == student_id)
        student = db.exec(statement).first()
        db.delete(student)
        db.commit()
        return {"message": f"{student} deleted successfully"}


@app.patch("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student: Student):
    ''' This function is used to update a student by id in the database'''
    with Session(engine) as db:
        statement = select(Students).where(Students.id == student_id)
        student_db = db.exec(statement).first()
        # student_db.id = student.id
        student_db.firstname = student.firstname
        student_db.lastname = student.lastname
        db.add(student_db)
        db.commit()
        db.refresh(student_db)
        return student_db
