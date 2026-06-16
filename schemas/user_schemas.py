from pydantic import BaseModel, Field
from typing import Optional

# Schema base com campos comuns
class UserBase(BaseModel):
    nome: str
    username: str
    categoria: str

# Schema para criação de usuário (exige senha)
class UserCreate(UserBase):
    senha: str

# Schema para atualização (senha é opcional)
class UserUpdate(BaseModel):
    nome: Optional[str] = None
    username: Optional[str] = None
    categoria: Optional[str] = None
    senha: Optional[str] = None
    ativo: Optional[bool] = None

# Schema para resposta da API (nunca inclui a senha)
class User(UserBase):
    id: int
    ativo: bool

    class Config:
        orm_mode = True
