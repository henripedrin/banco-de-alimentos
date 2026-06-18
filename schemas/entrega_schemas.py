from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# --- Schemas para Respostas da API ---

class EntregaPendenteResponse(BaseModel):
    id: int
    cesta_id: int
    recebedor_nome: str
    status: str
    data_criacao: datetime

class ItemCesta(BaseModel):
    nome: str
    quantidade_retirada: int

class EntregaDetalhesResponse(BaseModel):
    id: int
    cesta_id: int
    recebedor_nome: str
    operador_nome: Optional[str]
    status: str
    data_criacao: datetime
    data_entrega: Optional[datetime]
    observacao: Optional[str]
    itens_cesta: List[ItemCesta]

# --- Schemas para Ações (Corpo da Requisição) ---
# Não são necessários para esta feature, mas mantidos por consistência

class EntregaCreate(BaseModel):
    operador_id: int
    recebedor_id: int
    cesta_id: int

class EntregaConfirm(BaseModel):
    entrega_id: int

class EntregaCancel(BaseModel):
    entrega_id: int
    observacao: str
