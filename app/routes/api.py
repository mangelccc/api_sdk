from fastapi import APIRouter
from app.api.controllers.ControllerChat import ChatController
from app.api.controllers.ControllerUsuario import UserController

# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["api"])

# ========== RUTAS DE CHAT ==========
router.post("/chat", tags=["chat"])(ChatController.chat)
router.get("/agent-info", tags=["chat"])(ChatController.agent_info)

# ========== RUTAS DE USUARIOS - ESTILO LARAVEL ==========
router.get("/users", tags=["users"])(UserController.index)
router.get("/users/{user_id}", tags=["users"])(UserController.show)
router.post("/users", tags=["users"])(UserController.store)  # ← CORREGIDO: store en lugar de create
router.put("/users/{user_id}", tags=["users"])(UserController.update)
router.delete("/users/{user_id}", tags=["users"])(UserController.destroy)  # ← CORREGIDO: destroy en lugar de delete