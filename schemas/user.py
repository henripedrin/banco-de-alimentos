from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str
    username: str


class User(BaseModel):
    id: int
    name: str
    username: str
