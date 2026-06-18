from repository.entrega_repository import EntregaRepository
from schemas.entrega_schemas import EntregaDetalhesResponse
from fastapi import HTTPException, status

class EntregaService:
    def __init__(self):
        self.repository = EntregaRepository()

    def get_entregas_pendentes(self):
        entregas = self.repository.get_entregas_pendentes()
        return entregas if entregas else []

    def get_entrega_detalhes(self, entrega_id: int):
        entrega_data = self.repository.get_entrega_by_id(entrega_id)
        if not entrega_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega não encontrada.")
        
        itens_cesta = self.repository.get_alimentos_by_cesta_id(entrega_data['cesta_id'])
        
        response = EntregaDetalhesResponse(
            **entrega_data,
            itens_cesta=itens_cesta if itens_cesta else []
        )
        return response

    def confirmar_entrega(self, entrega_id: int, operador_id: int):
        result = self.repository.confirmar_entrega(entrega_id, operador_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega não encontrada ou já foi processada.")
        return {"id": entrega_id, "status": "ENTREGUE", "message": "Entrega confirmada com sucesso!"}
