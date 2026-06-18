from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_profile(token: str = Depends(oauth2_scheme)):
    pass

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.get("/dashboard/administrador", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="admin_dashboard.html", context={"request": request})

@router.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin_usuarios.html", context={"request": request})

@router.get("/dashboard/nutricionista", response_class=HTMLResponse)
async def nutricionista_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="nutricionista_dashboard.html", context={"request": request})

@router.get("/dashboard/agente_sanitario", response_class=HTMLResponse)
async def agente_sanitario_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="agente_sanitario_dashboard.html", context={"request": request})

@router.get("/agente/validar", response_class=HTMLResponse)
async def agente_validacao_page(request: Request):
    return templates.TemplateResponse(request=request, name="agente_validacao.html", context={"request": request})

@router.get("/dashboard/operador_logistico", response_class=HTMLResponse)
async def operador_logistico_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="operador_logistico_dashboard.html", context={"request": request})

@router.get("/dashboard/recebedor", response_class=HTMLResponse)
async def recebedor_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="recebedor_dashboard.html", context={"request": request})

@router.get("/dashboard/doador", response_class=HTMLResponse)
async def doador_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="doador_dashboard.html", context={"request": request})

@router.get("/doador/doar", response_class=HTMLResponse)
async def doador_doacao_page(request: Request):
    return templates.TemplateResponse(request=request, name="doador_doacao.html", context={"request": request})

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})
