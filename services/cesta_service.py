from repository.cesta_repository import CestaRepository
from schemas.cesta_schema import CestaRequest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CestaService:

    def __init__(self):
        self.repository = CestaRepository()

    def create_cesta(self, request: CestaRequest):
        """
        Orquestra a criação de uma cesta básica de forma transacional.
        """
        try:
            logger.info("Iniciando a criação da cesta básica.")
            cesta_id = self.repository.create_cesta_transactional(request.cesta, request.alimentos)
            logger.info(f"Cesta básica criada com sucesso. ID: {cesta_id}")
            return {"cesta_id": cesta_id, "message": "Cesta básica criada com sucesso."}
        except Exception as e:
            logger.error(f"Erro ao criar a cesta básica: {e}")
            raise e
