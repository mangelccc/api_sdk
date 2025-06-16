from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes import router

def create_app() -> FastAPI:
    # Inicializar FastAPI
    app = FastAPI(title="Chat Agent API", version="1.0.0")

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir rutas
    app.include_router(router)

    return app

# Handler para AWS Lambda
app = create_app()
handler = Mangum(app)
