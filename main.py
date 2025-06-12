import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi.encoders import jsonable_encoder
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

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not vector_store_id:
    raise ValueError("VECTOR_STORE_ID not found in environment variables")

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = api_key

# Create the agent
agent = Agent(
    name="Agente Ejemplo",
    instructions="responde con feo siempre al final y con menos de 5 palabras.",
    model="gpt-4.1-nano-2025-04-14",
)

# Modelos Pydantic
class Book(BaseModel):
    name: str
    genre: Literal["fiction", "non-fiction"]
    price: float
    book_id: Optional[str] = uuid4().hex

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    respuesta: str

# Configuración de archivos y datos
BOOKS_FILE = "books.json"
BOOKS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

# Inicializar FastAPI
app = FastAPI(title="Bookstore API with Chat Agent", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handler para AWS Lambda (si es necesario)
handler = Mangum(app)

# Rutas existentes de la librería
@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app with AI chat!"}

@app.get("/random-book")
async def random_book():
    if not BOOKS:
        raise HTTPException(404, "No books available")
    return random.choice(BOOKS)

@app.get("/list-books")
async def list_books():
    return {"books": BOOKS}

@app.get("/book_by_index/{index}")
async def book_by_index(index: int):
    if index < len(BOOKS):
        return BOOKS[index]
    else:
        raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")

@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS.append(json_book)
    
    # Guardar en archivo
    try:
        with open(BOOKS_FILE, "w") as f:
            json.dump(BOOKS, f)
    except Exception as e:
        raise HTTPException(500, f"Error saving book: {str(e)}")
    
    return {"book_id": book.book_id}

@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOKS:
        if book.get("book_id") == book_id:
            return book
    raise HTTPException(404, f"Book ID {book_id} not found in database.")

# Nueva ruta para el chat agent
@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """
    Endpoint para interactuar con el agente de chat
    """
    try:
        user_input = chat_message.message
        
        if not user_input.strip():
            raise HTTPException(400, "Message cannot be empty")
        
        # Ejecutar el agente de forma asíncrona
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: Runner.run_sync(agent, user_input)
        )
        
        return ChatResponse(respuesta=result.final_output)
        
    except Exception as e:
        raise HTTPException(500, f"Chat agent error: {str(e)}")

# Ruta adicional para obtener información del agente
@app.get("/api/agent-info")
async def agent_info():
    """
    Obtiene información sobre el agente de chat
    """
    return {
        "name": agent.name,
        "instructions": agent.instructions,
        "model": agent.model,
        "status": "active"
    }

# Ruta para combinar libros y chat (ejemplo de integración)
@app.post("/api/chat-about-books")
async def chat_about_books(chat_message: ChatMessage):
    """
    Chat agent con contexto sobre los libros disponibles
    """
    try:
        user_input = chat_message.message
        
        # Agregar contexto de libros al mensaje
        books_context = f"Libros disponibles: {len(BOOKS)} libros. "
        if BOOKS:
            books_context += f"Géneros: {list(set(book.get('genre', 'unknown') for book in BOOKS))}. "
        
        enhanced_message = f"{books_context}Pregunta del usuario: {user_input}"
        
        # Ejecutar el agente
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: Runner.run_sync(agent, enhanced_message)
        )
        
        return ChatResponse(respuesta=result.final_output)
        
    except Exception as e:
        raise HTTPException(500, f"Chat agent error: {str(e)}")

# Ruta de salud del sistema
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "books_count": len(BOOKS),
        "agent_status": "active" if agent else "inactive"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
