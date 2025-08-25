from bson import ObjectId
from pymongo import ReturnDocument
from fastapi import HTTPException, Response
from app.utils.serializers import serialize_user
from app.db import users_collection
from app.models.user import User, UserIn, UserUpdate
from app.auth.security import hash_password

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

async def create_user(data: UserIn):
    existing = await users_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    data_dict = data.model_dump()
    data_dict["password"] = hash_password(data.password)
    data_dict["is_active"] = True

    result = await users_collection.insert_one(data_dict)
    new_user = await users_collection.find_one({"_id": result.inserted_id})
    return serialize_user(new_user)



async def get_all_user():
    cursor = users_collection.find().skip(0).limit(min(50, 100))
    print(cursor)
    users = []
    async for doc in cursor:
        users.append(serialize_user(doc))
    return users


async def update_user(user_id: str, data: dict):
    oid = ObjectId(user_id)
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    
    user = await users_collection.find_one_and_update(
        {"_id": oid}, {"$set": update_data}, return_document=ReturnDocument.AFTER
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)


async def delete_user(user_id: str):
    oid = ObjectId(user_id)
    user = await users_collection.find_one_and_delete({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)