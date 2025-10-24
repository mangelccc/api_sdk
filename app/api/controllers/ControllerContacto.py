from fastapi import HTTPException, Depends
from app.api.models.Contacto import Contacto, CreateContacto, UpdateContacto
from app.security import verify_token
from app.bd.conexion_bd_agents import get_db_connection
from app.services.ContactoEmailService import ContactoEmailService
import psycopg2.extras
from datetime import datetime

class ContactoController:
    
    @staticmethod
    def create(contacto_data: CreateContacto, token: str = Depends(verify_token)):
        """
        Crea un nuevo contacto y envía email de notificación
        ✅ AHORA SÍ REQUIERE TOKEN (protección anti-spam)
        ✅ Solo recibe nombre, email, telefono, mensaje (sin ID)
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Preparar datos (sin ID, se auto-genera)
            data = {
                'nombre': contacto_data.nombre,
                'email': contacto_data.email,
                'telefono': contacto_data.telefono,
                'mensaje': contacto_data.mensaje,
                'estado': 'PENDIENTE',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Insertar en base de datos (uuid e id se generan automáticamente)
            query = """
                INSERT INTO contactos (nombre, email, telefono, mensaje, estado, created_at, updated_at)
                VALUES (%(nombre)s, %(email)s, %(telefono)s, %(mensaje)s, %(estado)s, %(created_at)s, %(updated_at)s)
                RETURNING *
            """
            
            cursor.execute(query, data)
            row = cursor.fetchone()
            connection.commit()
            
            if not row:
                cursor.close()
                connection.close()
                raise HTTPException(status_code=500, detail="Error al crear el contacto")
            
            # Convertir el resultado a modelo
            contacto = Contacto(
                id=row['id'],
                uuid=row['uuid'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                mensaje=row['mensaje'],
                estado=row['estado'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
            cursor.close()
            connection.close()
            
            # Enviar email de notificación
            try:
                ContactoEmailService.send_contacto_notification(
                    nombre=contacto_data.nombre,
                    email=contacto_data.email,
                    telefono=contacto_data.telefono or "No proporcionado",
                    mensaje=contacto_data.mensaje
                )
            except Exception as email_error:
                # El contacto ya se guardó, pero falló el email
                print(f"Advertencia: Contacto guardado pero falló el envío de email: {email_error}")
            
            return {
                "message": "Contacto recibido exitosamente",
                "contacto": contacto,
                "status": 201
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear contacto: {str(e)}")
    
    @staticmethod
    def index(token: str = Depends(verify_token)):
        """
        Obtiene todos los contactos - REQUIERE TOKEN
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM contactos ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            if not rows:
                return {
                    "message": "No hay contactos registrados",
                    "contactos": [],
                    "status": 200
                }
            
            contactos = []
            for row in rows:
                contacto = Contacto(
                    id=row['id'],
                    uuid=row['uuid'],
                    nombre=row['nombre'],
                    email=row['email'],
                    telefono=row['telefono'],
                    mensaje=row['mensaje'],
                    estado=row['estado'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                contactos.append(contacto)
            
            return {
                "message": "Contactos obtenidos",
                "contactos": contactos,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    @staticmethod
    def show(contacto_id: int, token: str = Depends(verify_token)):
        """
        Obtiene un contacto específico por ID - REQUIERE TOKEN
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM contactos WHERE id = %s", (contacto_id,))
            row = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not row:
                return {
                    "message": "Contacto no encontrado",
                    "status": 404
                }
            
            contacto = Contacto(
                id=row['id'],
                uuid=row['uuid'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                mensaje=row['mensaje'],
                estado=row['estado'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
            return {
                "message": "Contacto encontrado",
                "contacto": contacto,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    @staticmethod
    def update(contacto_id: int, contacto_data: UpdateContacto, token: str = Depends(verify_token)):
        """
        Actualiza un contacto - REQUIERE TOKEN
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM contactos WHERE id = %s", (contacto_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Contacto no encontrado",
                    "status": 404
                }
            
            # Obtener datos validados
            data = contacto_data.dict(exclude_unset=True)
            
            if not data:
                cursor.close()
                connection.close()
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
            # Agregar timestamp de actualización
            data['updated_at'] = datetime.now()
            
            # Generar UPDATE dinámico
            set_clauses = [f"{column} = %s" for column in data.keys()]
            values = list(data.values()) + [contacto_id]
            
            query = f"""
                UPDATE contactos 
                SET {', '.join(set_clauses)}
                WHERE id = %s 
                RETURNING *
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            contacto = Contacto(
                id=row['id'],
                uuid=row['uuid'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                mensaje=row['mensaje'],
                estado=row['estado'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
            return {
                "message": "Contacto actualizado",
                "contacto": contacto,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar contacto: {str(e)}")
    
    @staticmethod
    def destroy(contacto_id: int, token: str = Depends(verify_token)):
        """
        Elimina un contacto - REQUIERE TOKEN
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM contactos WHERE id = %s", (contacto_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Contacto no encontrado",
                    "status": 404
                }
            
            # Eliminar
            cursor.execute("DELETE FROM contactos WHERE id = %s", (contacto_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "message": "Contacto eliminado",
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar contacto: {str(e)}")