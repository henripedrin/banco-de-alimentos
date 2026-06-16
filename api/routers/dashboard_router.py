from fastapi import APIRouter, Depends
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
    # Verifica se é admin (opcionalmente pode criar uma dependência específica para isso)
    if current_user.categoria != "ADMINISTRADOR":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Acesso negado")

    return service.get_admin_dashboard_data()
