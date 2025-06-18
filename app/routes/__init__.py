# Inicializa el paquete de rutas
from app.routes.routes import router as main_router

# Exportar el router principal para que factory.py pueda importarlo
router = main_router