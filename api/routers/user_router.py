from fastapi import APIRouter

from schemas.user_schemas import UserCreate, UserUpdate
from services.user_service import UserService
from schemas import user_schemas

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/", response_model=list[user_schemas.User])
def get_users():
    userService = UserService()
    return userService.get_users()

@router.get("/{id}/", response_model=user_schemas.User)
def get_user_by_username(username: str):
    userService = UserService()
    return userService.get_user_by_username(username)


@router.post("/", response_model=user_schemas.User)
def add_user(userCreate: UserCreate):
    userService = UserService()
    return userService.create_user(userCreate)

@router.put("/", response_model=UserUpdate)
def update_user(userUpdate: UserUpdate, username):
    userService = UserService()
    return userService.update_user(userUpdate, username)

@router.delete("/", response_model= user_schemas.User)
def delete_user(username: str):
    userService = UserService()
    return userService.delete_user(username)