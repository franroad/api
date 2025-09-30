from .. import schemas
from ..mail import conf
from fastapi_mail import FastMail,MessageSchema
from fastapi import APIRouter, Depends

router=APIRouter()

@router.post("/send-email")
async def send_email(message:schemas.EmailMessage):
    html = f"""
    <p>Hola ,</p>
    <p>Tu código para restablecer contraseña es: <strong></strong></p>
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