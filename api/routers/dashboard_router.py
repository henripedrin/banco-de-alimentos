from fastapi import APIRouter, Depends, HTTPException
from services.dashboard_service import DashboardService
from schemas.user_schemas import User
from api.dependencies import get_current_active_user

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])

@router.get("/admin")
def get_admin_dashboard(
    current_user: User = Depends(get_current_active_user),
    service: DashboardService = Depends()
):
    """
    Retorna os dados dinâmicos para o dashboard do administrador.
    Acesso restrito a usuários da categoria ADMINISTRADOR.
    """
    if current_user.categoria != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return service.get_admin_dashboard_data()

@router.get("/logistica")
def get_logistica_dashboard(
    current_user: User = Depends(get_current_active_user),
    service: DashboardService = Depends()
):
    """
    Retorna os dados dinâmicos para o dashboard do operador logístico.
    Acesso restrito a usuários da categoria OPERADOR_LOGISTICO.
    """
    if current_user.categoria != "OPERADOR_LOGISTICO":
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return service.get_logistica_dashboard_data()
