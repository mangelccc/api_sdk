from fastapi import APIRouter
from app.api.controllers.ControllerChat import ChatController
from app.api.controllers.ControllerUsuario import UsuarioController

# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["api"])

# ========== RUTAS DE CHAT ==========
router.post("/chat", tags=["chat"])(ChatController.chat)
router.get("/agent-info", tags=["chat"])(ChatController.agent_info)

# ========== RUTAS DE REGISTRO (SIN TOKEN) ==========
router.post("/usuarios/registro", tags=["registro"])(UsuarioController.registro)
router.get("/usuarios/verificar-email/{token}", tags=["registro"])(UsuarioController.verificar_email)

# ========== RUTAS DE USUARIOS - POR ID (ESTILO LARAVEL) ==========
router.get("/usuarios", tags=["usuarios"])(UsuarioController.index)
router.get("/usuarios/{usuario_id}", tags=["usuarios"])(UsuarioController.show)
router.post("/usuarios", tags=["usuarios"])(UsuarioController.store)
router.put("/usuarios/{usuario_id}", tags=["usuarios"])(UsuarioController.update)
router.delete("/usuarios/{usuario_id}", tags=["usuarios"])(UsuarioController.destroy)

# ========== RUTAS DE USUARIOS - POR UUID ==========
router.get("/usuarios/uuid/{usuario_uuid}", tags=["usuarios-uuid"])(UsuarioController.show_by_uuid)
router.put("/usuarios/uuid/{usuario_uuid}", tags=["usuarios-uuid"])(UsuarioController.update_by_uuid)
router.delete("/usuarios/uuid/{usuario_uuid}", tags=["usuarios-uuid"])(UsuarioController.destroy_by_uuid)