import aiosmtplib
import re

from email.message import EmailMessage
from email.utils import formataddr
from app.core.config import settings

SMTP_HOST       = settings.SMTP_HOST 
SMTP_PORT       = settings.SMTP_PORT
SMTP_USER       = settings.SMTP_USER 
SMTP_PASS       = settings.SMTP_PASS 
SMTP_FROM_NAME  = settings.SMTP_FROM_NAME 
SMTP_FROM_EMAIL = settings.SMTP_FROM_EMAIL 

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

async def send_email(to_email: str, subject: str, body: str, html: bool = False):
    
    message = EmailMessage()
    
    message["From"]     = formataddr( (settings.SMTP_FROM_NAME, settings.SMTP_FROM_EMAIL) )
    message["To"]       = to_email
    message["Subject"]  = subject

    if html:
        message.add_alternative(body, subtype="html") 
    else:
        message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USER,
        password=SMTP_PASS,
    )
    return True