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
        """Obtiene todos los usuarios - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            rows = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            if not rows:
                return {
                    "message": "No hay usuarios registrados",
                    "status": 200
                }
            
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
            
            return {
                "usuarios": usuarios,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def store(user_data: CreateUsuario, token: str = Depends(verify_token)):
        """Crea un nuevo usuario - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Obtener datos del modelo y preparar valores
            data = user_data.dict(exclude_unset=True)
            
            # Generar UUID si no existe
            if 'uuid' not in data or not data['uuid']:
                data['uuid'] = uuid.uuid4()
            
            # Convertir listas a JSON
            if 'cualidades' in data:
                data['cualidades'] = json.dumps(data['cualidades'])
            if 'funciones' in data:
                data['funciones'] = json.dumps(data['funciones'])
            
            # Agregar timestamps
            data['created_at'] = datetime.now()
            data['updated_at'] = datetime.now()
            
            # Generar INSERT dinámico
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ['%s'] * len(values)
            
            query = f"""
                INSERT INTO usuarios ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            
            if not row:
                cursor.close()
                connection.close()
                return {
                    "message": "Error al crear el usuario",
                    "status": 500
                }
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Convertir campos JSON de vuelta
            cualidades = json.loads(row.get('cualidades', '[]'))
            funciones = json.loads(row.get('funciones', '[]'))
            
            usuario = {
                "id": row['id'],
                "uuid": str(row['uuid']),
                "email": row['email'],
                "nombre": row['nombre'],
                "avatar": row['avatar'],
                "tipo": row['tipo'],
                "fecha_nacimiento": str(row['fecha_nacimiento']) if row['fecha_nacimiento'] else None,
                "link_linkedin": row['link_linkedin'],
                "link_github": row['link_github'],
                "tema": row['tema'],
                "idioma": row['idioma'],
                "mejorar_agente": row['mejorar_agente'],
                "instrucciones": row['instrucciones'],
                "apodo": row['apodo'],
                "oficio": row['oficio'],
                "cualidades": cualidades,
                "sobre_ti": row['sobre_ti'],
                "funciones": funciones,
                "memoria": row['memoria'],
                "provider": row['provider'],
                "provider_id": row['provider_id'],
                "created_at": str(row['created_at']),
                "updated_at": str(row['updated_at'])
            }
            
            return {
                "message": "Usuario creado",
                "usuario": usuario,
                "status": 201
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    @staticmethod
    def show(user_id: int, token: str = Depends(verify_token)):
        """Obtiene un usuario específico por ID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not row:
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
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
            
            return {
                "usuario": usuario,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def show_by_uuid(user_uuid: str, token: str = Depends(verify_token)):
        """Obtiene un usuario específico por UUID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios WHERE uuid = %s", (user_uuid,))
            row = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not row:
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
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
            
            return {
                "usuario": usuario,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def update(user_id: int, user_data: UpdateUsuario, token: str = Depends(verify_token)):
        """Actualiza un usuario completo por ID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
            # Obtener datos validados
            data = user_data.dict(exclude_unset=True)
            
            if not data:
                cursor.close()
                connection.close()
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
            # Convertir listas a JSON
            if 'cualidades' in data:
                data['cualidades'] = json.dumps(data['cualidades'])
            if 'funciones' in data:
                data['funciones'] = json.dumps(data['funciones'])
            
            # Agregar timestamp de actualización
            data['updated_at'] = datetime.now()
            
            # Generar UPDATE dinámico
            set_clauses = [f"{column} = %s" for column in data.keys()]
            values = list(data.values()) + [user_id]
            
            query = f"""
                UPDATE usuarios 
                SET {', '.join(set_clauses)}
                WHERE id = %s 
                RETURNING *
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            # Convertir campos JSON de vuelta
            cualidades = json.loads(row.get('cualidades', '[]'))
            funciones = json.loads(row.get('funciones', '[]'))
            
            usuario = {
                "id": row['id'],
                "uuid": str(row['uuid']),
                "email": row['email'],
                "nombre": row['nombre'],
                "avatar": row['avatar'],
                "tipo": row['tipo'],
                "fecha_nacimiento": str(row['fecha_nacimiento']) if row['fecha_nacimiento'] else None,
                "link_linkedin": row['link_linkedin'],
                "link_github": row['link_github'],
                "tema": row['tema'],
                "idioma": row['idioma'],
                "mejorar_agente": row['mejorar_agente'],
                "instrucciones": row['instrucciones'],
                "apodo": row['apodo'],
                "oficio": row['oficio'],
                "cualidades": cualidades,
                "sobre_ti": row['sobre_ti'],
                "funciones": funciones,
                "memoria": row['memoria'],
                "provider": row['provider'],
                "provider_id": row['provider_id'],
                "created_at": str(row['created_at']),
                "updated_at": str(row['updated_at'])
            }
            
            return {
                "message": "Usuario actualizado",
                "usuario": usuario,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

    @staticmethod
    def update_by_uuid(user_uuid: str, user_data: UpdateUsuario, token: str = Depends(verify_token)):
        """Actualiza un usuario completo por UUID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM usuarios WHERE uuid = %s", (user_uuid,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
            # Obtener datos validados
            data = user_data.dict(exclude_unset=True)
            
            if not data:
                cursor.close()
                connection.close()
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
            # Convertir listas a JSON
            if 'cualidades' in data:
                data['cualidades'] = json.dumps(data['cualidades'])
            if 'funciones' in data:
                data['funciones'] = json.dumps(data['funciones'])
            
            # Agregar timestamp de actualización
            data['updated_at'] = datetime.now()
            
            # Generar UPDATE dinámico
            set_clauses = [f"{column} = %s" for column in data.keys()]
            values = list(data.values()) + [user_uuid]
            
            query = f"""
                UPDATE usuarios 
                SET {', '.join(set_clauses)}
                WHERE uuid = %s 
                RETURNING *
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            # Convertir campos JSON de vuelta
            cualidades = json.loads(row.get('cualidades', '[]'))
            funciones = json.loads(row.get('funciones', '[]'))
            
            usuario = {
                "id": row['id'],
                "uuid": str(row['uuid']),
                "email": row['email'],
                "nombre": row['nombre'],
                "avatar": row['avatar'],
                "tipo": row['tipo'],
                "fecha_nacimiento": str(row['fecha_nacimiento']) if row['fecha_nacimiento'] else None,
                "link_linkedin": row['link_linkedin'],
                "link_github": row['link_github'],
                "tema": row['tema'],
                "idioma": row['idioma'],
                "mejorar_agente": row['mejorar_agente'],
                "instrucciones": row['instrucciones'],
                "apodo": row['apodo'],
                "oficio": row['oficio'],
                "cualidades": cualidades,
                "sobre_ti": row['sobre_ti'],
                "funciones": funciones,
                "memoria": row['memoria'],
                "provider": row['provider'],
                "provider_id": row['provider_id'],
                "created_at": str(row['created_at']),
                "updated_at": str(row['updated_at'])
            }
            
            return {
                "message": "Usuario actualizado",
                "usuario": usuario,
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

    @staticmethod
    def destroy(user_id: int, token: str = Depends(verify_token)):
        """Elimina un usuario por ID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
            # Eliminar
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "message": "Usuario eliminado",
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

    @staticmethod
    def destroy_by_uuid(user_uuid: str, token: str = Depends(verify_token)):
        """Elimina un usuario por UUID - Estilo Laravel"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que existe
            cursor.execute("SELECT id FROM usuarios WHERE uuid = %s", (user_uuid,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return {
                    "message": "Usuario no encontrado",
                    "status": 404
                }
            
            # Eliminar
            cursor.execute("DELETE FROM usuarios WHERE uuid = %s", (user_uuid,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                "message": "Usuario eliminado",
                "status": 200
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")