import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv('.env')

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = "buecher24@joekel.dev"
    MAIL_PORT = 587
    MAIL_SERVER = "email-smtp.eu-central-1.amazonaws.com"
    MAIL_FROM_NAME = "Bücher24"


async def send_email_async(subject: str, email_to: str, body: str):

    if Envs.MAIL_USERNAME is None or Envs.MAIL_PASSWORD is None:
        return

    conf = ConnectionConfig(
        MAIL_USERNAME=Envs.MAIL_USERNAME,
        MAIL_PASSWORD=Envs.MAIL_PASSWORD,
        MAIL_FROM=Envs.MAIL_FROM,
        MAIL_PORT=Envs.MAIL_PORT,
        MAIL_SERVER=Envs.MAIL_SERVER,
        MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
        MAIL_SSL_TLS=False,
        MAIL_STARTTLS=True,
        USE_CREDENTIALS=True)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='plain',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)