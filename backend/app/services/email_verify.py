import smtplib
from email.message import EmailMessage

from app.core.config import settings
def sent_verification_email(email:str,token:str):
    verification_link = f"http://localhost:8000/auth/verify_email?token={token}"
    msg=EmailMessage()
    msg['Subject']="Email Verification"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email
    msg.set_content(
    f"""
        Hi {email},

        Thank you for signing up.

        Please click the link below to verify your email:

        {verification_link}

        This verification link will expire in 30 minutes.

        If you did not create this account, you can safely ignore this email.

        Regards,
        Insurance Premium Predictor Team
        """
        )
    with smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USER,settings.EMAIL_PASSWORD)
        server.send_message(msg)