import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    # Diccionario simple para guardar tokens temporalmente (en producción usa Redis o BD)
    verification_tokens = {}
    
    @staticmethod
    def send_verification_email(email: str, user_data: dict):
        """
        Envía email de verificación - Súper simple
        """
        try:
            # Generar token único
            token = str(uuid.uuid4())
            
            # Guardar token con expiración (30 minutos)
            EmailService.verification_tokens[token] = {
                'email': email,
                'user_data': user_data,
                'expires_at': datetime.now() + timedelta(minutes=30)
            }
            
            # Configuración de email
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            if not smtp_user or not smtp_password:
                raise Exception("Configuración de email incompleta en .env")
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = "Verifica tu cuenta"
            
            # Cuerpo del email - Link dinámico
            base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
            verification_url = f"{base_url}/api/usuarios/verificar-email/{token}"
            
            body = f"""
            ¡Hola!
            
            Para activar tu cuenta, haz click aquí:
            
            {verification_url}
            
            Este enlace expira en 30 minutos.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_user, email, text)
            server.quit()
            
            return token
            
        except Exception as e:
            raise Exception(f"Error enviando email: {str(e)}")
    
    @staticmethod
    def verify_token(token: str):
        """
        Verifica si el token es válido y no ha expirado
        """
        if token not in EmailService.verification_tokens:
            return None
            
        token_data = EmailService.verification_tokens[token]
        
        # Verificar expiración
        if datetime.now() > token_data['expires_at']:
            # Limpiar token expirado
            del EmailService.verification_tokens[token]
            return None
            
        return token_data
    
    @staticmethod
    def consume_token(token: str):
        """
        Consume el token (lo elimina después de usarlo)
        """
        if token in EmailService.verification_tokens:
            token_data = EmailService.verification_tokens[token]
            del EmailService.verification_tokens[token]
            return token_data
        return None