from fastapi import APIRouter, Depends
from typing import List

from app.models.user import User, UserIn, UserUpdate
from app.auth.security import get_current_user
from app.services.user_service import create_user, get_user_by_id, get_user_by_email, get_all_user, update_user, delete_user


router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
async def register_user(user: UserIn):
    return await create_user(user)


@router.get("/all", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    print("Getting all users")
    return await get_all_user()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    return await get_user_by_id(user_id)


@router.put("/{user_id}", response_model=User)
async def update_user_data(user_id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    return await update_user(user_id, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user_data(user_id: str, current_user: User = Depends(get_current_user)):
    return await delete_user(user_id)