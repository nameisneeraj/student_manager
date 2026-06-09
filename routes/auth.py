from fastapi import APIRouter, HTTPException

from database import users_collection
from models.user import User
from utils.security import hash_password

router = APIRouter(
    tags=["Athuentication"]
)

@router.post("/register")
def register(user: User):

    existing_user = users_collection()


