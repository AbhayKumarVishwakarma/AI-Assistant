from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel

from app.auth.Token import Token
from app.auth.security import create_access_token, verify_password
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.services.user_service import get_user_by_email
from app.auth.security import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # print("Access token expires minutes: ", access_token_expires)
    token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer", "username": user["username"]}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
