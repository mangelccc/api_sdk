import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("VECTOR_STORE_ID")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

# Validaciones
if not AUTH_TOKEN:
    raise ValueError("API_AUTH_TOKEN not found in environment variables. Add it to your .env.local file")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not vector_store_id:
    raise ValueError("VECTOR_STORE_ID not found in environment variables")

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = api_key
