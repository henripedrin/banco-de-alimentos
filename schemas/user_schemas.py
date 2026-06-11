from pydantic import BaseModel

class UserCreate(BaseModel):
    nome: str
    username: str
    senha: str
    categoria: str


class User(BaseModel):
    id: int
    nome: str
    username: str
    senha: str
    categoria: str
    ativo: bool


class UserUpdate(BaseModel):
    nome: str
