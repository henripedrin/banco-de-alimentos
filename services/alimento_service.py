from repository.alimento_repository import FoodRepository
from schemas.alimento_schemas import LoteCreate


class AlimentoService:
    def get_validade(self):
        foodRepository = FoodRepository()
        return foodRepository.get_validade()

    def create_lote(self, lote: LoteCreate):
        foodRepository = FoodRepository()
        return foodRepository.save_food(lote)
