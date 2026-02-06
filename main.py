from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
students_db: dict[int, dict] = {}
current_id = 1


class Student(BaseModel):
    name: str
    email: str
    age: int
    roll_number: str
    dept: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    roll_number: str
    dept: str


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/student", response_model=StudentResponse)
def create_student(student: Student):
    global current_id
    student_data = student.model_dump()
    student_data["id"] = current_id
    students_db[current_id] = student_data
    current_id += 1
    return student_data


@app.get("/student/{id}", response_model=StudentResponse)
def get_student(id: int):
    if id not in students_db:
        return {"error": "Student not found"}
    return students_db[id]


@app.get("/students", response_model=List[StudentResponse])
def get_all_students():
    return list(students_db.values())


@app.put("/student/{id}", response_model=StudentResponse)
def update_student(id: int, student: Student):
    if id not in students_db:
        return {"error": "Student not found"}
    student_data = student.model_dump()
    student_data["id"] = id
    students_db[id] = student_data
    return student_data


@app.delete("/student/{id}")
def delete_student(id: int):
    if id not in students_db:
        return {"error": "Student not found"}
    deleted_student = students_db.pop(id)
    return {"message": "Student deleted", "student": deleted_student}
