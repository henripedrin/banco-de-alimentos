from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.api import api_router  # Importa o roteador principal da API
from api.routers import web_router  # Importa o roteador da interface web

app = FastAPI(
    title="Banco de Alimentos",
    description="Sistema para gestão de alimentos",
    version="1.0.0"
)

# Monta o diretório static para servir CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclui o roteador da API sob o prefixo /api/v1
app.include_router(api_router, prefix="/api/v1")

# Inclui o roteador da interface web na raiz
app.include_router(web_router.router)
