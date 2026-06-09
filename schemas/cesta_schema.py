from pydantic import BaseModel


class CestaCreate(BaseModel):
    nutricionista_id: int
    recebedor_id: int


class AlimentoCestaCreate(BaseModel):
    cesta_id: int
    alimento_id: int
    quantidade_retirada: int

class ListaAlimentosCestaCreate(BaseModel):
    alimentos: list[AlimentoCestaCreate]