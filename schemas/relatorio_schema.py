from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional

class Relatorio(BaseModel):
    id: int
    file_name: str
    reference_month: str
    generation_date: datetime
    file_path: str

    class Config:
        orm_mode = True

class GerarRelatorioRequest(BaseModel):
    start_date: date
    end_date: date

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('A data final deve ser posterior à data inicial.')
        return v
