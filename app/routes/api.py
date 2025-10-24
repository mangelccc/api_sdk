from fastapi import APIRouter
from app.api.controllers.ControllerChat import ChatController
from app.api.controllers.ControllerUsuario import UsuarioController
from app.api.controllers.ControllerContacto import ContactoController


# Crear router para rutas de API
router = APIRouter(prefix="/api", tags=["api"])

# ========== RUTAS DE CHAT ==========
router.post("/chat", tags=["chat"])(ChatController.chat)
router.get("/agent-info", tags=["chat"])(ChatController.agent_info)

# ========== RUTAS DE REGISTRO (SIN TOKEN) ==========
router.post("/usuarios/registro", tags=["registro"])(UsuarioController.registro)
router.get("/usuarios/verificar-email/{token}", tags=["registro"])(UsuarioController.verificar_email)

router.post("/usuarios/login", tags=["auth"])(UsuarioController.login)

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

# ========== RUTAS DE CONTACTO ✅ TODAS CON TOKEN ==========
router.post("/contactos", tags=["contacto"])(ContactoController.create)          # ✅ Crear contacto (CON TOKEN)
router.get("/contactos", tags=["contacto"])(ContactoController.index)            # ✅ Listar contactos (CON TOKEN)
router.get("/contactos/{contacto_id}", tags=["contacto"])(ContactoController.show)
router.put("/contactos/{contacto_id}", tags=["contacto"])(ContactoController.update)
router.delete("/contactos/{contacto_id}", tags=["contacto"])(ContactoController.destroy)
