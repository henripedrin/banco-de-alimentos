from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from reports.scheduler import schedule_monthly_report, start_scheduler, shutdown_scheduler

from api.api import api_router
from api.routers import web_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado na inicialização
    schedule_monthly_report()
    start_scheduler()
    yield
    # Código a ser executado no encerramento
    shutdown_scheduler()

app = FastAPI(
    title="Banco de Alimentos",
    description="Sistema para gestão de alimentos",
    version="1.0.0",
    lifespan=lifespan
)

# Monta o diretório static para servir CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Monta o diretório de relatórios para permitir o download
app.mount("/relatorios", StaticFiles(directory="relatorios"), name="relatorios")

# Inclui os roteadores
app.include_router(api_router, prefix="/api/v1")
app.include_router(web_router.router)
