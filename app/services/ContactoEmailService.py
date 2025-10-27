import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class ContactoEmailService:
    
    @staticmethod
    def get_admin_email_template(nombre: str, email: str, telefono: str, mensaje: str) -> str:
        """
        Template HTML para notificación al ADMINISTRADOR
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
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <div class="emoji">📬</div>
                    <h1>¡Nuevo Contacto!</h1>
                </div>
                
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
                
                <div class="footer">
                    <p>Este es un correo automático generado por el sistema de contacto</p>
                    <p>Responde directamente al email del cliente para contactarlo</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_user_confirmation_template(nombre: str) -> str:
        """
        Template HTML para confirmación al USUARIO
        """
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mensaje Recibido</title>
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
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 20px;
                    text-align: center;
                }}
                
                .logo {{
                    width: 250px;
                    height: 250px;
                    margin: 0 auto 15px auto;
                    display: block;
                }}
                
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                
                .header h1 {{
                    color: white;
                    font-size: 32px;
                    font-weight: 700;
                    margin: 0 0 10px 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }}
                
                .header p {{
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 16px;
                }}
                
                .content {{
                    padding: 40px 30px;
                }}
                
                .greeting {{
                    font-size: 22px;
                    color: #333;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}
                
                .message {{
                    font-size: 16px;
                    color: #555;
                    line-height: 1.8;
                    margin-bottom: 25px;
                }}
                
                .info-box {{
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                    border-left: 4px solid #667eea;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 25px 0;
                }}
                
                .info-box h3 {{
                    color: #667eea;
                    font-size: 18px;
                    margin-bottom: 12px;
                }}
                
                .info-box ul {{
                    list-style: none;
                    padding-left: 0;
                }}
                
                .info-box li {{
                    color: #555;
                    font-size: 15px;
                    margin-bottom: 8px;
                    padding-left: 25px;
                    position: relative;
                }}
                
                .info-box li:before {{
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #667eea;
                    font-weight: bold;
                    font-size: 18px;
                }}
                
                .cta-section {{
                    text-align: center;
                    margin: 30px 0;
                    padding: 25px;
                    background: #f8f9fa;
                    border-radius: 12px;
                }}
                
                .cta-section p {{
                    color: #666;
                    font-size: 15px;
                    margin-bottom: 15px;
                }}
                
                .social-links {{
                    margin-top: 15px;
                    text-align: center;
                }}
                
                .social-links table {{
                    margin: 0 auto;
                    border-spacing: 15px 0;
                }}
                
                .social-link {{
                    display: inline-block;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 25px;
                    font-size: 14px;
                    font-weight: 600;
                    transition: transform 0.3s ease;
                }}
                
                .social-link:hover {{
                    transform: translateY(-2px);
                }}
                
                .footer {{
                    background: #f8f9fa;
                    padding: 25px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                
                .footer p {{
                    color: #999;
                    font-size: 13px;
                    margin: 5px 0;
                }}
                
                .timestamp {{
                    background: white;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 12px;
                    text-align: center;
                    margin-bottom: 25px;
                    font-size: 13px;
                    color: #666;
                }}
                
                @media only screen and (max-width: 600px) {{
                    .email-container {{
                        margin: 0;
                        border-radius: 0;
                    }}
                    
                    .header {{
                        padding: 30px 15px;
                    }}
                    
                    .content {{
                        padding: 30px 20px;
                    }}
                    
                    .header h1 {{
                        font-size: 26px;
                    }}
                    
                    .greeting {{
                        font-size: 20px;
                    }}
                    
                    .social-links table {{
                        border-spacing: 0 !important;
                    }}
                    
                    .social-links table tr {{
                        display: block;
                    }}
                    
                    .social-links table td {{
                        display: block;
                        padding: 5px 0 !important;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <img src="https://i.ibb.co/qYz0VnYk/Gemini-Generated-Image-uk4eqeuk4eqeuk4e-Photoroom.png" alt="ZeroWork Logo" class="logo">
                    <h1>¡Mensaje Recibido!</h1>
                    <p>Gracias por contactarnos</p>
                </div>
                
                <div class="content">
                    <div class="timestamp">
                        📅 {fecha_hora}
                    </div>
                    
                    <div class="greeting">
                        ¡Hola {nombre}! 👋
                    </div>
                    
                    <div class="message">
                        Hemos recibido tu mensaje correctamente. Nuestro equipo lo revisará y 
                        te responderemos lo antes posible.
                    </div>
                    
                    <div class="info-box">
                        <h3>📋 ¿Qué sigue ahora?</h3>
                        <ul>
                            <li>Revisaremos tu consulta en detalle</li>
                            <li>Te responderemos en un plazo de 24-48 horas</li>
                            <li>Recibirás nuestra respuesta en este mismo email</li>
                        </ul>
                    </div>
                    
                    <div class="cta-section">
                        <p><strong>Mientras tanto, síguenos en nuestras redes:</strong></p>
                        <div class="social-links">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                                <tr>
                                    <td style="padding: 0 7.5px;">
                                        <a href="https://www.zerowork.es" class="social-link">🌐 Web</a>
                                    </td>
                                    <td style="padding: 0 7.5px;">
                                        <a href="https://www.linkedin.com/in/grimalmiguel" class="social-link">💼 LinkedIn</a>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    
                    <div class="message" style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                        Si tienes alguna pregunta urgente, no dudes en responder directamente a este correo.
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Gracias por tu confianza</strong></p>
                    <p>Este es un correo automático, pero puedes responderlo directamente</p>
                    <p style="margin-top: 15px;">
                        © 2025 ZeroWork • Todos los derechos reservados
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def send_contacto_notification(nombre: str, email: str, telefono: str, mensaje: str):
        """
        Envía 2 emails:
        1. Notificación al ADMINISTRADOR con los datos del contacto
        2. Confirmación al USUARIO de que recibimos su mensaje
        """
        try:
            # Configuración de email
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            if not smtp_user or not smtp_password:
                raise Exception("⚠️ Configuración de email incompleta en .env")
            
            print(f"📧 Iniciando envío de emails...")
            print(f"📤 SMTP: {smtp_server}:{smtp_port}")
            print(f"👤 Desde: {smtp_user}")
            
            # ============================================
            # 1️⃣ EMAIL AL ADMINISTRADOR
            # ============================================
            destino_admin = "zeroworkia@gmail.com"
            
            msg_admin = MIMEMultipart('alternative')
            msg_admin['From'] = f"Sistema de Contacto <{smtp_user}>"
            msg_admin['To'] = destino_admin
            msg_admin['Subject'] = f"Nuevo contacto de {nombre}"
            msg_admin['Reply-To'] = email
            
            html_admin = ContactoEmailService.get_admin_email_template(
                nombre, email, telefono, mensaje
            )
            
            text_admin = f"""
NUEVO CONTACTO RECIBIDO

Nombre: {nombre}
Email: {email}
Teléfono: {telefono if telefono else 'No proporcionado'}

Mensaje:
{mensaje}

---
Recibido el {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """
            
            part1_admin = MIMEText(text_admin, 'plain', 'utf-8')
            part2_admin = MIMEText(html_admin, 'html', 'utf-8')
            msg_admin.attach(part1_admin)
            msg_admin.attach(part2_admin)
            
            # ============================================
            # 2️⃣ EMAIL DE CONFIRMACIÓN AL USUARIO
            # ============================================
            msg_user = MIMEMultipart('alternative')
            msg_user['From'] = f"ZeroWork<{smtp_user}>"
            msg_user['To'] = email
            msg_user['Subject'] = f"Mensaje recibido - Gracias {nombre}"
            msg_user['Reply-To'] = smtp_user
            
            html_user = ContactoEmailService.get_user_confirmation_template(nombre)
            
            text_user = f"""
¡Hola {nombre}!

Hemos recibido tu mensaje correctamente. 

Nuestro equipo lo revisará y te responderemos lo antes posible 
(generalmente en 24-48 horas).

Gracias por contactarnos.

---
ZeroWork
{datetime.now().strftime("%d/%m/%Y %H:%M")}
            """
            
            part1_user = MIMEText(text_user, 'plain', 'utf-8')
            part2_user = MIMEText(html_user, 'html', 'utf-8')
            msg_user.attach(part1_user)
            msg_user.attach(part2_user)
            
            # ============================================
            # 📬 ENVIAR AMBOS EMAILS
            # ============================================
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.set_debuglevel(1)  # Ver logs detallados
            server.starttls()
            server.login(smtp_user, smtp_password)
            
            # Enviar al admin
            print(f"\n📤 Enviando a ADMIN: {destino_admin}")
            server.sendmail(smtp_user, destino_admin, msg_admin.as_string())
            print(f"Email al admin enviado correctamente")
            
            # Enviar al usuario
            print(f"\n📤 Enviando confirmación a USUARIO: {email}")
            server.sendmail(smtp_user, email, msg_user.as_string())
            print(f"Email de confirmación enviado correctamente")
            
            server.quit()
            print(f"\n🎉 ¡Ambos emails enviados exitosamente!")
            
            return True
            
        except smtplib.SMTPException as e:
            print(f"\n❌ Error SMTP: {str(e)}")
            raise Exception(f"Error SMTP enviando emails: {str(e)}")
        except Exception as e:
            print(f"\n❌ Error general: {str(e)}")
            raise Exception(f"Error enviando emails: {str(e)}")