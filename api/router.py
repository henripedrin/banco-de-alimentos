from fastapi import APIRouter

from api.routers import auth_router, user_router, admin_index_route

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(user_router.router)
api_router.include_router(admin_index_route.router)