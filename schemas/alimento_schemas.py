from datetime import date

from pydantic import BaseModel


class AlimentoResponse(BaseModel):
    nome: str
    quantidade: int
    data_vencimento: date


class AlimentoCreate(BaseModel):
    nome: str
    categoria_id: int
    quantidade: int
    unidade_medida: str
    data_vencimento: date


class LoteCreate(BaseModel):
    alimentos: list[AlimentoCreate]