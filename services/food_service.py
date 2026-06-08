from repository.food_repository import FoodRepository


class FoodService:
    def get_validade(self):
        foodRepository = FoodRepository()
        return foodRepository.get_validade()