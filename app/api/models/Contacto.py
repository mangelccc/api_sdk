from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class Contacto(BaseModel):
    """Modelo completo de Contacto"""
    id: Optional[int] = Field(None, description="ID auto-generado")
    uuid: Optional[UUID] = Field(None, description="UUID auto-generado")
    nombre: str = Field(..., min_length=2, max_length=255, description="Nombre del contacto")
    email: EmailStr = Field(..., description="Email del contacto")
    telefono: Optional[str] = Field(None, max_length=50, description="Teléfono opcional")
    mensaje: str = Field(..., min_length=10, description="Mensaje del contacto")
    estado: str = Field(default="PENDIENTE", description="Estado: PENDIENTE, CONTACTADO, CERRADO")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")

    class Config:
        from_attributes = True

class CreateContacto(BaseModel):
    """Modelo para crear un contacto (solo campos requeridos)"""
    nombre: str = Field(..., min_length=2, max_length=255, description="Nombre del contacto")
    email: EmailStr = Field(..., description="Email del contacto")
    telefono: Optional[str] = Field(None, max_length=50, description="Teléfono opcional")
    mensaje: str = Field(..., min_length=10, description="Mensaje del contacto")

class UpdateContacto(BaseModel):
    """Modelo para actualizar un contacto (todos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=50)
    mensaje: Optional[str] = Field(None, min_length=10)
    estado: Optional[str] = Field(None, description="PENDIENTE, CONTACTADO, CERRADO")

class ContactoResponse(BaseModel):
    """Respuesta estándar para operaciones de contacto"""
    message: str
    contacto: Optional[Contacto] = None
    status: int