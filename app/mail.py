from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from . config import settings
from . import schemas

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,   # activa STARTTLS
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
)



async def send_email(code):
    html = f"""
    <p>Hola ,</p>
    <p>Tu código para restablecer contraseña es: <strong>{code}</strong></p>
    <p>Expira en 15 minutos.</p>
    """

    

    email = MessageSchema(
        subject="Passqord Recovery",
        recipients=["franco.fran@gmail.com"],
        body=html,
        subtype="html"
    )

    print(email)
    
    fm = FastMail(conf)
    
    await fm.send_message(email)
    return {"message": "email has been sent"}