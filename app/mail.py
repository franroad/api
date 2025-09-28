from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME = "8tsxu9vyjpqhpbdz",
    MAIL_PASSWORD = "gtvegqoetp7uibsj",
    MAIL_FROM = "fbernal.jmzafra@gmail.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailmug.net",
    MAIL_STARTTLS=False,   # activa STARTTLS
    MAIL_SSL_TLS=False,
)

