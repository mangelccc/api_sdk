from fastapi import APIRouter
from app.api.models import ChatResponse
from app.api.controllers.chat_controller import ChatController

# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["chat"])

# Usar los métodos del controlador directamente como manejadores de ruta
router.post("/chat", response_model=ChatResponse)(ChatController.chat)
router.get("/agent-info")(ChatController.agent_info)