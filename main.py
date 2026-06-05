from fastapi import FastAPI

from api.router import api_router
from routers import auth_router

app = FastAPI(
    title="Banco de Alimentos",
    description="Sistema para gestão de alimentos",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

