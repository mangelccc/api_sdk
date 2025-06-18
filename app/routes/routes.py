from fastapi import APIRouter
from app.routes.api import router as api_router

# Router principal para la aplicación
router = APIRouter()

# Incluir las rutas de la API con el prefijo /api
router.include_router(api_router)

# Aquí puedes agregar rutas directas (sin el prefijo /api)
@router.get("/", tags=["root"])
async def root():
    """
    Ruta principal de la aplicación
    """
    return {
        "message": "Bienvenido a la API de Chat Agents",
        "docs": "/docs",
        "api_endpoints": "/api"
    }

# Puedes agregar más rutas directas aquí según sea necesario