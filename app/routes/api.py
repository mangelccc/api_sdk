from fastapi import APIRouter
from app.api.controllers.ControllerChat import ChatController
from app.api.controllers.ControllerUsuario import UserController

# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["api"])

# ========== RUTAS DE CHAT ==========
router.post("/chat", tags=["chat"])(ChatController.chat)
router.get("/agent-info", tags=["chat"])(ChatController.agent_info)

# ========== RUTAS DE USUARIOS - POR ID (ESTILO LARAVEL) ==========
router.get("/users", tags=["users"])(UserController.index)
router.get("/users/{user_id}", tags=["users"])(UserController.show)
router.post("/users", tags=["users"])(UserController.store)
router.put("/users/{user_id}", tags=["users"])(UserController.update)
router.delete("/users/{user_id}", tags=["users"])(UserController.destroy)

# ========== RUTAS DE USUARIOS - POR UUID ==========
router.get("/users/uuid/{user_uuid}", tags=["users-uuid"])(UserController.show_by_uuid)
router.put("/users/uuid/{user_uuid}", tags=["users-uuid"])(UserController.update_by_uuid)
router.delete("/users/uuid/{user_uuid}", tags=["users-uuid"])(UserController.destroy_by_uuid)