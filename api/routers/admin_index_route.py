from fastapi import APIRouter

from services.food_service import FoodService
from schemas.food_schemas import FoodResponse

router = APIRouter(prefix="/admin_index", tags=["admin_index"])

@router.get("/", response_model=list[FoodResponse])
def get_validade():
    foodService = FoodService()
    return foodService.get_validade()