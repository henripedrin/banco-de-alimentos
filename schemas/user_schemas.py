from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    username: str
    senha: str
    categoria: str


class User(BaseModel):
    id: int
    name: str
    username: str
    senha: str
    categoria: str
    ativo: bool


class UserUpdate(BaseModel):
    name: str
