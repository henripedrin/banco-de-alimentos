from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

class AlimentoDoacaoCreate(BaseModel):
    nome: str
    categoria_id: int
    quantidade: int
    unidade_medida: str
    data_vencimento: date


class DoacaoCreate(BaseModel):
    doador_nome: str
    itens_solicitacao: list[AlimentoDoacaoCreate]

class DoacaoSucessoResponse(BaseModel):
    mensagem: str
    solicitacao_id: int


class DoacaoResponse(BaseModel):
    doador_id: int
    data_solicitacao: datetime
    status: str
    observacao_vigilante: Optional[str]