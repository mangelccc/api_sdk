from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import date, datetime
from uuid import UUID

class Usuario(BaseModel):
    # Campos auto-generados (solo lectura)
    id: Optional[int] = Field(None, description="Solo lectura - Auto generado")
    uuid: Optional[UUID] = Field(None, description="Opcional - Se genera automático si no se envía")
    created_at: Optional[datetime] = Field(None, description="Solo lectura - Auto generado")
    updated_at: Optional[datetime] = Field(None, description="Solo lectura - Auto generado")
        
    # Campo requerido para crear (opcional para actualizar)
    email: Optional[EmailStr] = Field(None, description="Requerido para crear usuario")
    contrasena: Optional[str] = Field(None, description="Requerida para crear usuario")
        
    # Campos opcionales con defaults
    nombre: Optional[str] = None
    avatar: Optional[str] = None
    tipo: str = "USUARIO"
    fecha_nacimiento: Optional[date] = None
    link_linkedin: Optional[str] = None
    link_github: Optional[str] = None
    tema: str = "DEFAULT"
    idioma: str = "ES"
    mejorar_agente: bool = False
    instrucciones: Optional[str] = None
    apodo: Optional[str] = None
    oficio: Optional[str] = None
    cualidades: List[Any] = []
    sobre_ti: Optional[str] = None
    funciones: List[Any] = []
    memoria: bool = False
    provider: Optional[str] = None
    provider_id: Optional[str] = None

    class Config:
        from_attributes = True

# Modelo para crear un usuario (campos requeridos)
class CreateUsuario(BaseModel):
    email: EmailStr = Field(..., description="Email requerido")
    contrasena: str = Field(..., min_length=6, description="Contraseña requerida (mínimo 6 caracteres)")
    
    # Campos opcionales para creación
    uuid: Optional[UUID] = None
    nombre: Optional[str] = None
    avatar: Optional[str] = None
    tipo: str = "USUARIO"
    fecha_nacimiento: Optional[date] = None
    link_linkedin: Optional[str] = None
    link_github: Optional[str] = None
    tema: str = "DEFAULT"
    idioma: str = "ES"
    mejorar_agente: bool = False
    instrucciones: Optional[str] = None
    apodo: Optional[str] = None
    oficio: Optional[str] = None
    cualidades: List[Any] = []
    sobre_ti: Optional[str] = None
    funciones: List[Any] = []
    memoria: bool = False
    provider: Optional[str] = None
    provider_id: Optional[str] = None

# Modelo para actualizar un usuario (todos los campos opcionales excepto ID)
class UpdateUsuario(BaseModel):
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = Field(None, min_length=6)
    nombre: Optional[str] = None
    avatar: Optional[str] = None
    tipo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    link_linkedin: Optional[str] = None
    link_github: Optional[str] = None
    tema: Optional[str] = None
    idioma: Optional[str] = None
    mejorar_agente: Optional[bool] = None
    instrucciones: Optional[str] = None
    apodo: Optional[str] = None
    oficio: Optional[str] = None
    cualidades: Optional[List[Any]] = None
    sobre_ti: Optional[str] = None
    funciones: Optional[List[Any]] = None
    memoria: Optional[bool] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
