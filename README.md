# 🤖 Chat Agents SDK API

Una API REST construida con **FastAPI** que proporciona endpoints para interactuar con agentes de chat basados en **OpenAI GPT**. Diseñada para funcionar como backend de aplicaciones de chat en React.

## 🎯 **¿Para qué sirve?**

Esta API permite a aplicaciones frontend (especialmente **React**) enviar mensajes a agentes de IA y recibir respuestas inteligentes. Perfecta para:

- 💬 Chatbots personalizados
- 🤖 Asistentes virtuales
- 🎨 Agentes especializados por temas
- 📱 Aplicaciones de chat en tiempo real

## 🔗 **Frontend React**

Esta API está diseñada para funcionar con nuestra aplicación React de chat:

**🔗 [Repositorio React Chat Frontend](https://github.com/mangelccc/react_sdk)** 

## 🚀 **Inicio Rápido**

### **Prerequisitos**
- Python 3.8+
- Cuenta OpenAI con API Key

### **Instalación**

```bash
# 1. Clonar repositorio
git clone <URL_DEL_REPO>
cd fastapi-chat

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores
```

### **Configuración (.env)**

```env
OPENAI_API_KEY=tu_openai_api_key_aqui
VECTOR_STORE_ID=tu_vector_store_id_aqui  
API_AUTH_TOKEN=tu_token_secreto_aqui
```

> ⚠️ **IMPORTANTE:** Para obtener el `API_AUTH_TOKEN` debes contactarme.

### **Ejecutar**

```bash
# Desarrollo
python main.py

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000

# Background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

## 📡 **Endpoints API**

### **🔐 Autenticación**
Todos los endpoints requieren un token Bearer en el header:
```bash
Authorization: Bearer tu_token_secreto
```

### **💬 Chat con Agente**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Hola, ¿cómo estás?"
}
```

**Respuesta:**
```json
{
  "respuesta": "¡Hola! Estoy bien, feo"
}
```

### **ℹ️ Información del Agente**
```http
GET /api/agent-info
```

**Respuesta:**
```json
{
  "name": "Agente Ejemplo",
  "instructions": "responde con feo siempre al final y con menos de 5 palabras.",
  "model": "gpt-4.1-nano-2025-04-14",
  "status": "active"
}
```

## 🛠 **Ejemplos de Uso**

### **JavaScript/React**

```javascript
fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer tu_token_secreto'
    },
    body: JSON.stringify({ message })
  });
  
  const data = await response.json();
  return data.respuesta;
}
```

### **cURL**

```bash
# Enviar mensaje
curl -X POST "http://localhost:8000/api/chat" \
  -H "Authorization: Bearer tu_token_secreto" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué tiempo hace?"}'

# Obtener info del agente
curl -X GET "http://localhost:8000/api/agent-info" \
  -H "Authorization: Bearer tu_token_secreto"
```

## 📁 **Estructura del Proyecto**

```
fastapi-chat/
├── main.py              # Punto de entrada
├── app/
│   ├── __init__.py
│   ├── config.py        # Variables de entorno
│   ├── security.py      # Autenticación
│   ├── models.py        # Modelos Pydantic
│   ├── agents.py        # Configuración del agente
│   ├── routes.py        # Endpoints API
│   └── factory.py       # Configuración de la app
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ **Configuración Avanzada**

### **Personalizar Agente**

Edita `app/agents.py`:

```python
agent = Agent(
    name="Tu Agente Personalizado",
    instructions="Instrucciones específicas para tu agente",
    model="gpt-4.1-nano-2025-04-14",
)
```

### **CORS para React**

La API está configurada para aceptar requests desde cualquier origen. En producción, especifica tu dominio en `app/factory.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Solo React dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🐳 **Docker** *(Opcional)*

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Construir y ejecutar
docker build -t fastapi-chat .
docker run -p 8000:8000 --env-file .env fastapi-chat
```

## 🔧 **Desarrollo**

### **Agregar Nuevos Agentes**

1. Crear nuevo agente en `app/agents.py`
2. Agregar rutas específicas en `app/routes.py`
3. Actualizar modelos si es necesario

## 📚 **Tecnologías Utilizadas**

- **FastAPI** - Framework web moderno para Python
- **OpenAI** - API para modelos de IA
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **Mangum** - Adaptador para AWS Lambda

---

**🔗 ¿Buscas el frontend React?** → [React Chat Frontend](ENLACE_AL_REPO_REACT)
