from fastapi import HTTPException, Depends
from app.api.models.User import Usuario, UsuariosResponse, CreateUsuario, UpdateUsuario
from app.security import verify_token
from app.bd.conexion_bd_agents import get_db_connection
import psycopg2.extras
import json
import uuid
from datetime import datetime

class UserController:
    @staticmethod
    def index(token: str = Depends(verify_token)):
        """
        Obtiene todos los usuarios de la base de datos
        Este método está diseñado para ser usado directamente como un manejador de ruta
        """
        connection = None
        cursor = None
        
        try:
            # Establecer conexión
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Ejecutar consulta
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            rows = cursor.fetchall()
            
            # Convertir a lista de objetos Usuario
            usuarios = []
            for row in rows:
                # Convertir campos JSON si existen
                cualidades = row.get('cualidades', [])
                if isinstance(cualidades, str):
                    try:
                        cualidades = json.loads(cualidades)
                    except:
                        cualidades = []
                
                funciones = row.get('funciones', [])
                if isinstance(funciones, str):
                    try:
                        funciones = json.loads(funciones)
                    except:
                        funciones = []
                
                usuario = Usuario(
                    id=row.get('id'),
                    uuid=row.get('uuid'),
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at'),
                    email=row.get('email'),
                    contrasena=row.get('contrasena'),  # En producción no devolver la contraseña
                    nombre=row.get('nombre'),
                    avatar=row.get('avatar'),
                    tipo=row.get('tipo', 'USUARIO'),
                    fecha_nacimiento=row.get('fecha_nacimiento'),
                    link_linkedin=row.get('link_linkedin'),
                    link_github=row.get('link_github'),
                    tema=row.get('tema', 'DEFAULT'),
                    idioma=row.get('idioma', 'ES'),
                    mejorar_agente=row.get('mejorar_agente', False),
                    instrucciones=row.get('instrucciones'),
                    apodo=row.get('apodo'),
                    oficio=row.get('oficio'),
                    cualidades=cualidades,
                    sobre_ti=row.get('sobre_ti'),
                    funciones=funciones,
                    memoria=row.get('memoria', False),
                    provider=row.get('provider'),
                    provider_id=row.get('provider_id')
                )
                usuarios.append(usuario)
            
            return UsuariosResponse(usuarios=usuarios, total=len(usuarios))
            
        except psycopg2.Error as db_error:
            raise HTTPException(
                status_code=500, 
                detail=f"Error de base de datos: {str(db_error)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno del servidor: {str(e)}"
            )
        finally:
            # Cerrar cursor y conexión
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def show(user_id: int, token: str = Depends(verify_token)):
        """
        Obtiene un usuario específico por ID
        """
        connection = None
        cursor = None
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Convertir campos JSON si existen
            cualidades = row.get('cualidades', [])
            if isinstance(cualidades, str):
                try:
                    cualidades = json.loads(cualidades)
                except:
                    cualidades = []
            
            funciones = row.get('funciones', [])
            if isinstance(funciones, str):
                try:
                    funciones = json.loads(funciones)
                except:
                    funciones = []
            
            usuario = Usuario(
                id=row.get('id'),
                uuid=row.get('uuid'),
                created_at=row.get('created_at'),
                updated_at=row.get('updated_at'),
                email=row.get('email'),
                contrasena=row.get('contrasena'),  # En producción no devolver la contraseña
                nombre=row.get('nombre'),
                avatar=row.get('avatar'),
                tipo=row.get('tipo', 'USUARIO'),
                fecha_nacimiento=row.get('fecha_nacimiento'),
                link_linkedin=row.get('link_linkedin'),
                link_github=row.get('link_github'),
                tema=row.get('tema', 'DEFAULT'),
                idioma=row.get('idioma', 'ES'),
                mejorar_agente=row.get('mejorar_agente', False),
                instrucciones=row.get('instrucciones'),
                apodo=row.get('apodo'),
                oficio=row.get('oficio'),
                cualidades=cualidades,
                sobre_ti=row.get('sobre_ti'),
                funciones=funciones,
                memoria=row.get('memoria', False),
                provider=row.get('provider'),
                provider_id=row.get('provider_id')
            )
            
            return usuario
            
        except psycopg2.Error as db_error:
            raise HTTPException(
                status_code=500, 
                detail=f"Error de base de datos: {str(db_error)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno del servidor: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def create(user_data: CreateUsuario, token: str = Depends(verify_token)):
        """
        Crea un nuevo usuario
        """
        connection = None
        cursor = None
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Generar UUID si no se proporcionó
            user_uuid = user_data.uuid if user_data.uuid else uuid.uuid4()
            
            # Convertir listas a JSON
            cualidades_json = json.dumps(user_data.cualidades) if user_data.cualidades else '[]'
            funciones_json = json.dumps(user_data.funciones) if user_data.funciones else '[]'
            
            # TODO: En producción, hashear la contraseña antes de guardarla
            # from werkzeug.security import generate_password_hash
            # hashed_password = generate_password_hash(user_data.contrasena)
            
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
            
            # Convertir campos JSON de vuelta
            cualidades = json.loads(row.get('cualidades', '[]'))
            funciones = json.loads(row.get('funciones', '[]'))
            
            usuario = Usuario(
                id=row['id'],
                uuid=row['uuid'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                email=row['email'],
                contrasena=row['contrasena'],
                nombre=row['nombre'],
                avatar=row['avatar'],
                tipo=row['tipo'],
                fecha_nacimiento=row['fecha_nacimiento'],
                link_linkedin=row['link_linkedin'],
                link_github=row['link_github'],
                tema=row['tema'],
                idioma=row['idioma'],
                mejorar_agente=row['mejorar_agente'],
                instrucciones=row['instrucciones'],
                apodo=row['apodo'],
                oficio=row['oficio'],
                cualidades=cualidades,
                sobre_ti=row['sobre_ti'],
                funciones=funciones,
                memoria=row['memoria'],
                provider=row['provider'],
                provider_id=row['provider_id']
            )
            
            return usuario
            
        except psycopg2.IntegrityError as integrity_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"Error de integridad (posiblemente email duplicado): {str(integrity_error)}"
            )
        except psycopg2.Error as db_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error de base de datos: {str(db_error)}"
            )
        except Exception as e:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno del servidor: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def update(user_id: int, user_data: UpdateUsuario, token: str = Depends(verify_token)):
        """
        Actualiza un usuario existente
        """
        connection = None
        cursor = None
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Crear query dinámico solo con campos que no son None
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
            
            # Agregar updated_at
            update_fields.append("updated_at = %s")
            update_values.append(datetime.now())
            update_values.append(user_id)
            
            query = f"""
                UPDATE usuarios 
                SET {', '.join(update_fields)}
                WHERE id = %s 
                RETURNING *
            """
            
            cursor.execute(query, update_values)
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            connection.commit()
            
            # Convertir campos JSON de vuelta
            cualidades = json.loads(row.get('cualidades', '[]'))
            funciones = json.loads(row.get('funciones', '[]'))
            
            usuario = Usuario(
                id=row['id'],
                uuid=row['uuid'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                email=row['email'],
                contrasena=row['contrasena'],
                nombre=row['nombre'],
                avatar=row['avatar'],
                tipo=row['tipo'],
                fecha_nacimiento=row['fecha_nacimiento'],
                link_linkedin=row['link_linkedin'],
                link_github=row['link_github'],
                tema=row['tema'],
                idioma=row['idioma'],
                mejorar_agente=row['mejorar_agente'],
                instrucciones=row['instrucciones'],
                apodo=row['apodo'],
                oficio=row['oficio'],
                cualidades=cualidades,
                sobre_ti=row['sobre_ti'],
                funciones=funciones,
                memoria=row['memoria'],
                provider=row['provider'],
                provider_id=row['provider_id']
            )
            
            return usuario
            
        except psycopg2.IntegrityError as integrity_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"Error de integridad: {str(integrity_error)}"
            )
        except psycopg2.Error as db_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error de base de datos: {str(db_error)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno del servidor: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def delete(user_id: int, token: str = Depends(verify_token)):
        """
        Elimina un usuario existente
        """
        connection = None
        cursor = None
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Primero verificar que el usuario existe
            cursor.execute("SELECT id, email, nombre FROM usuarios WHERE id = %s", (user_id,))
            user_exists = cursor.fetchone()
            
            if not user_exists:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Eliminar el usuario
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            connection.commit()
            
            return {
                "message": "Usuario eliminado exitosamente",
                "deleted_user_id": user_id,
                "deleted_user_email": user_exists['email'],
                "deleted_user_name": user_exists['nombre']
            }
            
        except psycopg2.Error as db_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error de base de datos: {str(db_error)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno del servidor: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()