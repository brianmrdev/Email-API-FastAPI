import logging
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
from .settings import settings
from .sanitizer import sanitize_html
from fastapi import HTTPException, status

# Modelo de datos para el envío de correos
class EmailSchema(BaseModel):
    from_email: EmailStr
    to_email: list[EmailStr]
    subject: str
    html: str

async def send_email(email: EmailSchema):
    logging.info(f"Attempting to send email from {email.from_email} to {email.to_email}")
    
    # Sanitizar el HTML antes de enviarlo
    sanitized_html = sanitize_html(email.html)

    smtp = SMTP(hostname=settings.smtp_host, port=settings.smtp_port, start_tls=False, use_tls=False)
    
    try:
        await smtp.connect()
        await smtp.starttls()
        await smtp.login(settings.smtp_username, settings.smtp_password)

        message = MIMEText(sanitized_html, "html")
        message["From"] = email.from_email
        message["To"] = ", ".join(email.to_email)
        message["Subject"] = email.subject

        await smtp.send_message(message)
        await smtp.quit()

        logging.info(f"Email sent successfully to {email.to_email}")
        return {"detail": {"message": "Email sent successfully", "status": status.HTTP_200_OK}}
    
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Error sending email: {str(e)}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
        )
