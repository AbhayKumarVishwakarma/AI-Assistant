from fastapi import APIRouter
from typing import List

from app.models.user import User, UserIn, UserUpdate
from app.services.user_service import create_user, get_user_by_id, get_user_by_email, get_all_user, update_user, delete_user


router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
async def register_user(user: UserIn):
    return await create_user(user)


@router.get("/all", response_model=List[User])
async def get_users():
    print("Getting all users")
    return await get_all_user()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    return await get_user_by_id(user_id)


@router.put("/{user_id}", response_model=User)
async def update_user_data(user_id: str, user: UserUpdate):
    return await update_user(user_id, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user_data(user_id: str):
    return await delete_user(user_id)