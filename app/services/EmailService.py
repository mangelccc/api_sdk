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
    def get_email_template(verification_url: str, user_name: str = "Usuario") -> str:
        """
        Template HTML moderno y responsivo para el email de verificación
        """
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verifica tu cuenta</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 20px;
                    text-align: center;
                }}
                
                .logo {{
                    width: 60px;
                    height: 60px;
                    background-color: white;
                    border-radius: 50%;
                    margin: 0 auto 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    font-weight: bold;
                    color: #667eea;
                }}
                
                .header h1 {{
                    color: white;
                    font-size: 28px;
                    margin: 0;
                    font-weight: 300;
                }}
                
                .content {{
                    padding: 40px 30px;
                }}
                
                .greeting {{
                    font-size: 18px;
                    color: #555;
                    margin-bottom: 20px;
                }}
                
                .message {{
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.8;
                }}
                
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    padding: 15px 40px;
                    border-radius: 50px;
                    font-size: 16px;
                    font-weight: 600;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    margin: 20px 0;
                }}
                
                .cta-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }}
                
                .alternative-link {{
                    margin-top: 30px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }}
                
                .alternative-link p {{
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 10px;
                }}
                
                .alternative-link a {{
                    color: #667eea;
                    word-break: break-all;
                    text-decoration: none;
                }}
                
                .footer {{
                    background-color: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                
                .footer p {{
                    color: #999;
                    font-size: 14px;
                    margin-bottom: 10px;
                }}
                
                .security-note {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                }}
                
                .security-note p {{
                    color: #856404;
                    font-size: 14px;
                    margin: 0;
                }}
                
                .icon {{
                    font-size: 18px;
                    margin-right: 8px;
                }}
                
                @media only screen and (max-width: 600px) {{
                    .email-container {{
                        margin: 0;
                        box-shadow: none;
                    }}
                    
                    .header {{
                        padding: 30px 15px;
                    }}
                    
                    .content {{
                        padding: 30px 20px;
                    }}
                    
                    .header h1 {{
                        font-size: 24px;
                    }}
                    
                    .cta-button {{
                        display: block;
                        width: 100%;
                        padding: 18px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <!-- Header -->
                <div class="header">
                    <div class="logo">✉️</div>
                    <h1>Verifica tu cuenta</h1>
                </div>
                
                <!-- Content -->
                <div class="content">
                    <div class="greeting">
                        ¡Hola {user_name}! 👋
                    </div>
                    
                    <div class="message">
                        Te damos la bienvenida a nuestra plataforma. Para completar tu registro y activar tu cuenta, 
                        necesitamos verificar tu dirección de correo electrónico.
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="cta-button">
                            <span class="icon">🔓</span>
                            Verificar mi cuenta
                        </a>
                    </div>
                    
                    <div class="security-note">
                        <p>
                            <strong>⏰ Importante:</strong> Este enlace expira en 30 minutos por tu seguridad.
                        </p>
                    </div>
                    
                    <div class="alternative-link">
                        <p><strong>¿No puedes hacer clic en el botón?</strong></p>
                        <p>Copia y pega este enlace en tu navegador:</p>
                        <a href="{verification_url}">{verification_url}</a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <p>Si no creaste esta cuenta, puedes ignorar este correo de forma segura.</p>
                    <p>Este es un correo automático, por favor no respondas a esta dirección.</p>
                    <p style="margin-top: 20px;">
                        <strong>Tu Aplicación</strong> • 
                        <a href="#" style="color: #667eea; text-decoration: none;">Política de Privacidad</a> • 
                        <a href="#" style="color: #667eea; text-decoration: none;">Términos de Servicio</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def send_verification_email(email: str, user_data: dict):
        """
        Envía email de verificación con diseño HTML moderno
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
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Tu Aplicación <{smtp_user}>"
            msg['To'] = email
            msg['Subject'] = "🔐 Verifica tu cuenta - ¡Solo un paso más!"
            
            # URL de verificación
            base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
            verification_url = f"{base_url}/api/usuarios/verificar-email/{token}"
            
            # Obtener nombre del usuario (si está disponible)
            user_name = user_data.get('nombre', user_data.get('name', 'Usuario'))
            
            # Crear versión HTML del email
            html_body = EmailService.get_email_template(verification_url, user_name)
            
            # Crear versión de texto plano como fallback
            text_body = f"""
¡Hola {user_name}!

Para activar tu cuenta, visita este enlace:
{verification_url}

Este enlace expira en 30 minutos.

Si no creaste esta cuenta, puedes ignorar este correo.

Saludos,
Tu Aplicación
            """
            
            # Adjuntar ambas versiones
            part1 = MIMEText(text_body, 'plain', 'utf-8')
            part2 = MIMEText(html_body, 'html', 'utf-8')
            
            msg.attach(part1)
            msg.attach(part2)
            
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