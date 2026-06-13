from fastapi import APIRouter, HTTPException, Depends, Query
from models.student import Student ,StudentResponse, StudentListResponse, UpdateStudentResponse
from database import students_collection
from typing import Optional
from dependencies.auth import (get_current_user)
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from bson.errors import InvalidId



router = APIRouter()

@router.get("/students", response_model=StudentListResponse)
def view_all(
    current_user: str = Depends(get_current_user), 
    search: str | None = None,
    sort_by: str | None = None,
    order: str = "asc",
    course: str | None = None, 
    age: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):

    filters = {}

    if search:
        filters["name"] = {
            "$regex": search,
            "$options": "i"
        }


    if course:
        filters["course"] = course

    if age is not None: 
        filters["age"] = age

    total = students_collection.count_documents(filters)
    
    query = students_collection.find(filters)

    if sort_by:
        sort_order = ASCENDING if order.lower() == "asc" else DESCENDING
        query = query.sort(sort_by, sort_order)


    students = list(
        query.skip(skip).limit(limit)
    )
    
    for student in students:
        if "_id" in student:
            student["id"] = str(student.pop("_id"))
    
    return {
    "total": total,
    "skip": skip,
    "limit": limit,
    "data": students
}

    


@router.post("/students")
def add(
    newstudent: Student,
    current_user: str = Depends(get_current_user)
):

    existing_student = students_collection.find_one({"name": newstudent.name})

    if existing_student:
        raise HTTPException(status_code=400, detail="Student Already Exists In DB")

    students_collection.insert_one(
        {"name": newstudent.name, "age": newstudent.age, "course": newstudent.course}
    )

    return {"message": "Student Added Successfully In DB", "student": newstudent}






@router.get("/students/{name}", response_model=StudentResponse)
def view_one(
    name: str,
    current_user: str = Depends(get_current_user)
):
    student = students_collection.find_one({"name": name})

    if not student:
        raise HTTPException(status_code=404, detail="Student Doesn't Exist In DB")

    student["_id"] = str(student["_id"])

    return student




@router.put(
        "/students/{student_id}", response_model=UpdateStudentResponse
)
def update_one(
    studentnewdata: Student,
    student_id: str,
    current_user: str = Depends(get_current_user)
):
    try:
        student_object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid Student ID"
        )

    student = students_collection.find_one(
        {"_id": student_object_id}
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student Doesn't Exist In DB"
        )
    
    existing_student = students_collection.find_one(
        {"name": studentnewdata.name}
    )

    if(
        existing_student and 
        str(existing_student["_id"] != student_id)
    ):
        raise HTTPException(
            status_code=400,
            detail="Student name already exists"
        )

    result = students_collection.update_one(
            {"_id": student_object_id},
            {
                "$set": {
                    "name": studentnewdata.name,
                    "age": studentnewdata.age,
                    "course": studentnewdata.course,
                }
            }
        )

    if result.modified_count == 0:
        return {
            "message": "No changes made",
            "student": {
                "id": student_id,
                "name": student["name"],
                "age": student["age"],
                "course": student["course"]
            }
        }
    
    return {
        "message": "Student Update Successfully",
        "student": {
            "id": student_id,
            "name": studentnewdata.name,
            "age": studentnewdata.age,
            "course": studentnewdata.course
        }
    }


@router.delete("/students/{student_id}")
def delete_one(
    student_id: str,
    current_user: str = Depends(get_current_user)
):
    try:
        student_object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid Student ID"
        )

    student = students_collection.find_one(
        {"_id": student_object_id}
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student Doesn't Exist In DB"
        )

    students_collection.delete_one(
        {"_id": student_object_id}
    )


    return {
    "message": "Student Deleted Successfully",
    "student_id": student_id,
    "student_name": student["name"]
}

