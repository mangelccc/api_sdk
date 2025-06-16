from fastapi import APIRouter, HTTPException, Depends
from app.models import ChatMessage, ChatResponse
from app.security import verify_token
from app.agents import agent
from agents import Runner
import asyncio

# Crear router
router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
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

@router.get("/agent-info")
async def agent_info(token: str = Depends(verify_token)):
    return {
        "name": agent.name,
        "instructions": agent.instructions,
        "model": agent.model,
        "status": "active"
    }
