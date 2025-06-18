from fastapi import HTTPException, Depends
from app.api.models.chat_model import ChatMessage, ChatResponse
from app.security import verify_token
from app.agents import agent
from agents import Runner
import asyncio

class ChatController:
    @staticmethod
    def chat(chat_message: ChatMessage, token: str = Depends(verify_token)):
        """
        Procesa un mensaje de chat usando el agente configurado
        Este método está diseñado para ser usado directamente como un manejador de ruta
        """
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
    
    @staticmethod
    async def agent_info(token: str = Depends(verify_token)):
        """
        Obtiene información sobre el agente configurado
        Este método está diseñado para ser usado directamente como un manejador de ruta
        """
        return {
            "name": agent.name,
            "instructions": agent.instructions,
            "model": agent.model,
            "status": "active"
        }