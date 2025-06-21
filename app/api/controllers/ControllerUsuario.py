from fastapi import HTTPException, Depends
from app.api.models.Usuario import Usuario, CreateUsuario, UpdateUsuario
from app.security import verify_token
from app.bd.conexion_bd_agents import get_db_connection
import psycopg2.extras
import json
import uuid
from datetime import datetime

class UserController:
    @staticmethod
    def index(token: str = Depends(verify_token)):
        """Obtiene todos los usuarios de la base de datos"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            rows = cursor.fetchall()
            
            usuarios = []
            for row in rows:
                # Convertir campos JSON
                cualidades = json.loads(row.get('cualidades', '[]')) if isinstance(row.get('cualidades'), str) else row.get('cualidades', [])
                funciones = json.loads(row.get('funciones', '[]')) if isinstance(row.get('funciones'), str) else row.get('funciones', [])
                
                usuario = {
                    "id": row.get('id'),
                    "uuid": str(row.get('uuid')) if row.get('uuid') else None,
                    "email": row.get('email'),
                    "nombre": row.get('nombre'),
                    "avatar": row.get('avatar'),
                    "tipo": row.get('tipo', 'USUARIO'),
                    "fecha_nacimiento": str(row.get('fecha_nacimiento')) if row.get('fecha_nacimiento') else None,
                    "link_linkedin": row.get('link_linkedin'),
                    "link_github": row.get('link_github'),
                    "tema": row.get('tema', 'DEFAULT'),
                    "idioma": row.get('idioma', 'ES'),
                    "mejorar_agente": row.get('mejorar_agente', False),
                    "instrucciones": row.get('instrucciones'),
                    "apodo": row.get('apodo'),
                    "oficio": row.get('oficio'),
                    "cualidades": cualidades,
                    "sobre_ti": row.get('sobre_ti'),
                    "funciones": funciones,
                    "memoria": row.get('memoria', False),
                    "provider": row.get('provider'),
                    "provider_id": row.get('provider_id'),
                    "created_at": str(row.get('created_at')) if row.get('created_at') else None,
                    "updated_at": str(row.get('updated_at')) if row.get('updated_at') else None
                }
                usuarios.append(usuario)
            
            cursor.close()
            connection.close()
            
            return {
                "data": {
                    "usuarios": usuarios,
                    "total": len(usuarios)
                },
                "status": "success",
                "message": f"Se encontraron {len(usuarios)} usuarios"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def show(user_id: int, token: str = Depends(verify_token)):
        """Obtiene un usuario específico por ID"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Convertir campos JSON
            cualidades = json.loads(row.get('cualidades', '[]')) if isinstance(row.get('cualidades'), str) else row.get('cualidades', [])
            funciones = json.loads(row.get('funciones', '[]')) if isinstance(row.get('funciones'), str) else row.get('funciones', [])
            
            usuario = {
                "id": row.get('id'),
                "uuid": str(row.get('uuid')) if row.get('uuid') else None,
                "email": row.get('email'),
                "nombre": row.get('nombre'),
                "avatar": row.get('avatar'),
                "tipo": row.get('tipo', 'USUARIO'),
                "fecha_nacimiento": str(row.get('fecha_nacimiento')) if row.get('fecha_nacimiento') else None,
                "link_linkedin": row.get('link_linkedin'),
                "link_github": row.get('link_github'),
                "tema": row.get('tema', 'DEFAULT'),
                "idioma": row.get('idioma', 'ES'),
                "mejorar_agente": row.get('mejorar_agente', False),
                "instrucciones": row.get('instrucciones'),
                "apodo": row.get('apodo'),
                "oficio": row.get('oficio'),
                "cualidades": cualidades,
                "sobre_ti": row.get('sobre_ti'),
                "funciones": funciones,
                "memoria": row.get('memoria', False),
                "provider": row.get('provider'),
                "provider_id": row.get('provider_id'),
                "created_at": str(row.get('created_at')) if row.get('created_at') else None,
                "updated_at": str(row.get('updated_at')) if row.get('updated_at') else None
            }
            
            cursor.close()
            connection.close()
            
            return {
                "data": usuario,
                "status": "success",
                "message": "Usuario encontrado exitosamente"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def create(user_data: CreateUsuario, token: str = Depends(verify_token)):
        """Crea un nuevo usuario"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Generar UUID si no se proporcionó
            user_uuid = user_data.uuid if user_data.uuid else uuid.uuid4()
            
            # Convertir listas a JSON
            cualidades_json = json.dumps(user_data.cualidades)
            funciones_json = json.dumps(user_data.funciones)
            
            cursor.execute("""
                INSERT INTO usuarios (
                    uuid, email, contrasena, nombre, avatar, tipo, fecha_nacimiento,
                    link_linkedin, link_github, tema, idioma, mejorar_agente, 
                    instrucciones, apodo, oficio, cualidades, sobre_ti, funciones,
                    memoria, provider, provider_id, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING *
            """, (
                user_uuid, user_data.email, user_data.contrasena, user_data.nombre,
                user_data.avatar, user_data.tipo, user_data.fecha_nacimiento,
                user_data.link_linkedin, user_data.link_github, user_data.tema,
                user_data.idioma, user_data.mejorar_agente, user_data.instrucciones,
                user_data.apodo, user_data.oficio, cualidades_json, user_data.sobre_ti,
                funciones_json, user_data.memoria, user_data.provider, user_data.provider_id,
                datetime.now(), datetime.now()
            ))
            
            row = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "data": {
                    "id": row['id'],
                    "uuid": str(row['uuid']),
                    "email": row['email'],
                    "nombre": row['nombre'],
                    "mensaje": "Usuario creado exitosamente"
                },
                "status": "success",
                "message": "Usuario creado exitosamente"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    @staticmethod
    def update(user_id: int, user_data: UpdateUsuario, token: str = Depends(verify_token)):
        """Actualiza un usuario existente"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Campos a actualizar
            update_fields = []
            update_values = []
            
            for field, value in user_data.dict(exclude_unset=True).items():
                if value is not None:
                    if field in ['cualidades', 'funciones']:
                        update_fields.append(f"{field} = %s")
                        update_values.append(json.dumps(value))
                    else:
                        update_fields.append(f"{field} = %s")
                        update_values.append(value)
            
            if not update_fields:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
            update_fields.append("updated_at = %s")
            update_values.append(datetime.now())
            update_values.append(user_id)
            
            query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE id = %s RETURNING id, email, nombre"
            cursor.execute(query, update_values)
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "data": {
                    "id": row['id'],
                    "email": row['email'],
                    "nombre": row['nombre'],
                    "mensaje": "Usuario actualizado exitosamente"
                },
                "status": "success",
                "message": "Usuario actualizado exitosamente"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

    @staticmethod
    def delete(user_id: int, token: str = Depends(verify_token)):
        """Elimina un usuario existente"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id, email, nombre FROM usuarios WHERE id = %s", (user_id,))
            user_exists = cursor.fetchone()
            
            if not user_exists:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Eliminar
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "data": {
                    "deleted_user_id": user_id,
                    "deleted_user_email": user_exists['email'],
                    "deleted_user_name": user_exists['nombre']
                },
                "status": "success",
                "message": "Usuario eliminado exitosamente"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")