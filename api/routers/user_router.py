from fastapi import APIRouter

from schemas.user import UserCreate, UserUpdate
from services.user_service import UserService
from schemas import user

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/", response_model=list[user.User])
def get_users():
    userService = UserService()
    return userService.get_users()

@router.get("/{id}/", response_model=user.User)
def get_user_by_username(username: str):
    userService = UserService()
    return userService.get_user_by_username(username)


@router.post("/", response_model=user.User)
def add_user(userCreate: UserCreate):
    userService = UserService()
    return userService.create_user(userCreate)

@router.put("/", response_model=UserUpdate)
def update_user(userUpdate: UserUpdate, username):
    userService = UserService()
    return userService.update_user(userUpdate, username)

@router.delete("/", response_model= user.User)
def delete_user(username: str):
    userService = UserService()
    return userService.delete_user(username)