from fastapi import APIRouter, HTTPException
from models.student import Student ,StudentResponse
from database import student_collections
from typing import Optional

router = APIRouter()

@router.get("/students", response_model=list[StudentResponse])
def view_all(course: str | None = None, age: int | None = None):

    filters = {}

    if course:
        filters["course"] = course

    if age: 
        filters["age"] = age

    if filters:
        students = list(
            student_collections.find(filters)
        )
    
    for student in students:
        student.pop("_id", None)
    
    return students

    


@router.post("/students")
def add(newstudent: Student):
    existing_student = student_collections.find_one({"name": newstudent.name})

    if existing_student:
        raise HTTPException(status_code=400, detail="Student Already Exists In DB")

    student_collections.insert_one(
        {"name": newstudent.name, "age": newstudent.age, "course": newstudent.course}
    )

    return {"message": "Student Added Successfully In DB", "student": newstudent}






@router.get("/students/{name}", response_model=StudentResponse)
def view_one(name: str):
    student = student_collections.find_one({"name": name})

    if not student:
        raise HTTPException(status_code=404, detail="Student Doesn't Exist In DB")

    student["_id"] = str(student["_id"])

    return student




@router.put("/students/{name}")
def update_one(studentnewdata: Student, name: str):
    student = student_collections.find_one({"name": name})

    if not student:
        raise HTTPException(status_code=404, detail="Student Doesn't Exist In DB")

    student_collections.update_one(
        {"name": name},
        {
            "$set": {
                "name": studentnewdata.name,
                "age": studentnewdata.age,
                "course": studentnewdata.course,
            }
        },
    )

    return {"message": "Student Updated Successfully", "student": studentnewdata}



@router.delete("/students/{name}")
def delete_one(name: str):
    student = student_collections.find_one({"name": name})

    if not student:
        raise HTTPException(status_code=404, detail="Student Doesn't Exist In DB")

    student_collections.delete_one({"name": name})

    return {"message": "Student Deleted Successfully"}

