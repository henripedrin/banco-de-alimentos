from fastapi import APIRouter

from .routers import (
    auth_router,
    user_router,
    admin_index_route,
    doacao_router,
    cesta_router,
    dashboard_router,
    categoria_router # Importando o router de categorias
)

# Este é o roteador principal para toda a API v1
api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(user_router.router)
api_router.include_router(admin_index_route.router)
api_router.include_router(doacao_router.router)
api_router.include_router(cesta_router.router)
api_router.include_router(dashboard_router.router)
api_router.include_router(categoria_router.router) # Registrando o router de categorias
