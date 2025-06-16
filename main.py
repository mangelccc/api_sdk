import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
import asyncio
from dotenv import load_dotenv

# Importaciones para el agente de chat
from agents import Agent, Runner, FileSearchTool

# Load environment variables
load_dotenv()

# Get configuration from environment
api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("VECTOR_STORE_ID")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

if not AUTH_TOKEN:
    raise ValueError("API_AUTH_TOKEN not found in environment variables. Add it to your .env.local file")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not vector_store_id:
    raise ValueError("VECTOR_STORE_ID not found in environment variables")

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = api_key

# Configurar seguridad
security = HTTPBearer()

# Función para verificar el token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Create the agent
agent = Agent(
    name="Agente Ejemplo",
    instructions="responde con feo siempre al final y con menos de 5 palabras.",
    model="gpt-4.1-nano-2025-04-14",
)

# Modelos Pydantic para Chat
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    respuesta: str

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

# Handler para AWS Lambda
handler = Mangum(app)

# ✅ SOLO RUTAS DE CHAT CON /api

@app.post("/api/chat", response_model=ChatResponse)
def chat(chat_message: ChatMessage, token: str = Depends(verify_token)):
    try:
        user_input = chat_message.message
        
        if not user_input.strip():
            raise HTTPException(400, "Message cannot be empty")
        
        # Crear event loop para el worker thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = Runner.run_sync(agent, user_input)
            return ChatResponse(respuesta=result.final_output)
        finally:
            loop.close()
            
    except Exception as e:
        raise HTTPException(500, f"Chat agent error: {str(e)}")

@app.get("/api/agent-info")
async def agent_info(token: str = Depends(verify_token)):
    return {
        "name": agent.name,
        "instructions": agent.instructions,
        "model": agent.model,
        "status": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)