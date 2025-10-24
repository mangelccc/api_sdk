import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class ContactoEmailService:
    
    @staticmethod
    def get_contacto_email_template(nombre: str, email: str, telefono: str, mensaje: str) -> str:
        """
        Template HTML moderno para notificación de nuevo contacto
        Colores: Gradientes morados/rosas/amarillos (como el código del modal)
        """
        telefono_display = telefono if telefono else "No proporcionado"
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nuevo Contacto</title>
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
                    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                    padding: 20px;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                    border-radius: 16px;
                    overflow: hidden;
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    box-shadow: 0 20px 50px rgba(88, 28, 135, 0.4);
                }}
                
                .header {{
                    background: linear-gradient(90deg, #fbbf24, #f472b6, #a855f7);
                    padding: 30px 20px;
                    text-align: center;
                }}
                
                .header h1 {{
                    color: white;
                    font-size: 28px;
                    font-weight: 700;
                    margin: 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }}
                
                .emoji {{
                    font-size: 48px;
                    margin-bottom: 10px;
                }}
                
                .content {{
                    padding: 40px 30px;
                    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
                }}
                
                .info-card {{
                    background: rgba(30, 27, 75, 0.6);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    backdrop-filter: blur(10px);
                }}
                
                .info-row {{
                    display: flex;
                    margin-bottom: 15px;
                    align-items: flex-start;
                }}
                
                .info-row:last-child {{
                    margin-bottom: 0;
                }}
                
                .info-label {{
                    font-weight: 600;
                    color: #fbbf24;
                    min-width: 100px;
                    font-size: 14px;
                }}
                
                .info-value {{
                    color: #f3f4f6;
                    font-size: 14px;
                    flex: 1;
                    word-break: break-word;
                }}
                
                .message-box {{
                    background: rgba(30, 27, 75, 0.8);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    border-left: 4px solid #a855f7;
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 20px;
                }}
                
                .message-title {{
                    color: #f472b6;
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 10px;
                }}
                
                .message-text {{
                    color: #d1d5db;
                    font-size: 15px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                }}
                
                .footer {{
                    background: rgba(15, 23, 42, 0.8);
                    padding: 20px;
                    text-align: center;
                    border-top: 1px solid rgba(168, 85, 247, 0.3);
                }}
                
                .footer p {{
                    color: #9ca3af;
                    font-size: 13px;
                    margin: 5px 0;
                }}
                
                .timestamp {{
                    background: linear-gradient(90deg, rgba(251, 191, 36, 0.1), rgba(244, 114, 182, 0.1), rgba(168, 85, 247, 0.1));
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                
                .timestamp-text {{
                    color: #fbbf24;
                    font-size: 13px;
                    font-weight: 500;
                }}
                
                @media only screen and (max-width: 600px) {{
                    .email-container {{
                        margin: 0;
                        border-radius: 0;
                    }}
                    
                    .header {{
                        padding: 25px 15px;
                    }}
                    
                    .content {{
                        padding: 30px 20px;
                    }}
                    
                    .header h1 {{
                        font-size: 24px;
                    }}
                    
                    .info-row {{
                        flex-direction: column;
                    }}
                    
                    .info-label {{
                        margin-bottom: 5px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <!-- Header -->
                <div class="header">
                    <div class="emoji">📬</div>
                    <h1>¡Nuevo Contacto!</h1>
                </div>
                
                <!-- Content -->
                <div class="content">
                    <div class="timestamp">
                        <p class="timestamp-text">📅 Recibido el {fecha_hora}</p>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-row">
                            <span class="info-label">👤 Nombre:</span>
                            <span class="info-value">{nombre}</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">📧 Email:</span>
                            <span class="info-value">{email}</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">📱 Teléfono:</span>
                            <span class="info-value">{telefono_display}</span>
                        </div>
                    </div>
                    
                    <div class="message-box">
                        <div class="message-title">💬 Mensaje:</div>
                        <div class="message-text">{mensaje}</div>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <p>Este es un correo automático generado por el sistema de contacto</p>
                    <p>Responde directamente al email del cliente para contactarlo</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def send_contacto_notification(nombre: str, email: str, telefono: str, mensaje: str):
        """
        Envía notificación de nuevo contacto a zeroworkia@gmail.com
        """
        try:
            # Configuración de email
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            if not smtp_user or not smtp_password:
                raise Exception("Configuración de email incompleta en .env")
            
            # Email destino
            destino = "zeroworkia@gmail.com"
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Sistema de Contacto <{smtp_user}>"
            msg['To'] = destino
            msg['Subject'] = f"🚀 Nuevo contacto de {nombre}"
            msg['Reply-To'] = email  # Para poder responder directamente al cliente
            
            # HTML del email
            html_body = ContactoEmailService.get_contacto_email_template(
                nombre, email, telefono, mensaje
            )
            
            # Texto plano como fallback
            text_body = f"""
NUEVO CONTACTO RECIBIDO

Nombre: {nombre}
Email: {email}
Teléfono: {telefono if telefono else 'No proporcionado'}

Mensaje:
{mensaje}

---
Recibido el {datetime.now().strftime("%d/%m/%Y %H:%M")}
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
            server.sendmail(smtp_user, destino, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error enviando email de contacto: {str(e)}")
            raise Exception(f"Error enviando email: {str(e)}")