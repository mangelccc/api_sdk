from fastapi import APIRouter
from app.api.models.Chat import ChatResponse
from app.api.models.User import Usuario, UsuariosResponse, CreateUsuario, UpdateUsuario, DeleteUsuarioResponse
from app.api.controllers.ControllerChat import ChatController
from app.api.controllers.ControllerUser import UserController

# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["api"])

# ========== RUTAS DE CHAT ==========
# Usar los métodos del controlador de chat directamente como manejadores de ruta
router.post("/chat", response_model=ChatResponse, tags=["chat"])(ChatController.chat)
router.get("/agent-info", tags=["chat"])(ChatController.agent_info)

# ========== RUTAS DE USUARIOS ==========
# Usar los métodos del controlador de usuarios directamente como manejadores de ruta
router.get("/users", response_model=UsuariosResponse, tags=["users"])(UserController.index)
router.get("/users/{user_id}", response_model=Usuario, tags=["users"])(UserController.show)
router.post("/users", response_model=Usuario, tags=["users"])(UserController.create)
router.put("/users/{user_id}", response_model=Usuario, tags=["users"])(UserController.update)
router.delete("/users/{user_id}", response_model=DeleteUsuarioResponse, tags=["users"])(UserController.delete)