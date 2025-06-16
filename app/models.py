from pydantic import BaseModel

# Modelos Pydantic para Chat
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    respuesta: str
