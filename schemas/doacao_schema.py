from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# --- Para Criação ---

class AlimentoDoacaoCreate(BaseModel):
    nome: str
    categoria_id: int
    quantidade: int = Field(..., gt=0)
    unidade_medida: str
    data_vencimento: date
    possui_avaria: bool = False
    quantidade_avariada: Optional[int] = Field(None, ge=0)
    descricao_avaria: Optional[str] = None

class DoacaoCreate(BaseModel):
    itens_solicitacao: List[AlimentoDoacaoCreate]

class DoacaoRejeitar(BaseModel):
    motivo: str = Field(..., min_length=10)

# --- Para Respostas ---

class DoacaoSucessoResponse(BaseModel):
    mensagem: str
    solicitacao_id: int

class ItemDoacao(BaseModel):
    nome: str
    quantidade: int
    unidade_medida: str

class DoacaoHistoryResponse(BaseModel):
    id: int
    data_solicitacao: datetime
    status: str
    observacao_vigilante: Optional[str] = None
    itens: List[ItemDoacao]

class ItemDoacaoDetalhes(ItemDoacao):
    categoria_id: int
    data_vencimento: date
    # Adicionar campos de avaria se necessário no futuro

class DoacaoDetalhesResponse(BaseModel):
    id: int
    data_solicitacao: datetime
    status: str
    observacao_vigilante: Optional[str] = None
    doador_nome: str
    itens: List[ItemDoacaoDetalhes]

class DoacaoPendente(BaseModel):
    id: int
    data_solicitacao: datetime
    doador_nome: str
    status: str

    class Config:
        orm_mode = True
