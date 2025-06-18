from fastapi import APIRouter
from app.api.models.Chat import ChatResponse
from app.api.controllers.ControllerChat import ControllerChat

# Crear router
router = APIRouter(prefix="/api", tags=["chat"])

# Usar los métodos del controlador directamente como manejadores de ruta
router.post("/chat", response_model=ChatResponse)(ControllerChat.chat)
router.get("/agent-info")(ControllerChat.agent_info)