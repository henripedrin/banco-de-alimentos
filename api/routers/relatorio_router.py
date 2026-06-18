from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List
from repository.relatorio_repository import RelatorioRepository
from schemas.relatorio_schema import Relatorio, GerarRelatorioRequest
from reports.generator import ReportGenerator
from api.dependencies import get_current_active_user
import os

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

REPORTS_DIR = "relatorios"

@router.get("/", response_model=List[Relatorio])
def get_all_relatorios(
    repo: RelatorioRepository = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    if current_user.categoria != "ADMINISTRADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    reports = repo.get_all_reports()
    return reports if reports else []

@router.post("/gerar")
def gerar_relatorio_manual(
    request: GerarRelatorioRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Inicia a geração de um relatório para um período customizado em background.
    """
    if current_user.categoria != "ADMINISTRADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    generator = ReportGenerator()
    # Adiciona a tarefa de geração pesada para ser executada em background
    background_tasks.add_task(
        generator.generate_report, 
        request.start_date, 
        request.end_date, 
        is_manual=True
    )
    
    return {"message": "A geração do relatório foi iniciada em segundo plano. A lista será atualizada em breve."}

@router.get("/download/{file_name}")
def download_relatorio(
    file_name: str,
    current_user: dict = Depends(get_current_active_user)
):
    if current_user.categoria != "ADMINISTRADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    file_path = os.path.join(REPORTS_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado.")
    
    return FileResponse(path=file_path, media_type='application/pdf', filename=file_name)
