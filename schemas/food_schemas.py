from datetime import date

from pydantic import BaseModel


class FoodResponse(BaseModel):
    name: str
    quantidade: int
    data_vencimento: date
