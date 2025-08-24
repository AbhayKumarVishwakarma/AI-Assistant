from app.models.user import User

def serialize_user(doc: dict) -> User:
    return User(
        id=str(doc["_id"]),
        username=doc["username"],
        email=doc["email"],
        is_active=doc["is_active"]
    )