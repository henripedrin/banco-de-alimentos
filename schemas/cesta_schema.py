from pydantic import BaseModel
from typing import List


class CestaCreate(BaseModel):
    nutricionista_id: int
    recebedor_id: int


class AlimentoCestaBase(BaseModel):
    alimento_id: int
    quantidade_retirada: int


class AlimentoCestaCreate(AlimentoCestaBase):
    cesta_id: int


class CestaRequest(BaseModel):
    cesta: CestaCreate
    alimentos: List[AlimentoCestaBase]


class ListaAlimentosCestaCreate(BaseModel):
    alimentos: List[AlimentoCestaCreate]
