import smtplib
from email.message import EmailMessage

from app.core.config import settings
def send_email(email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email
    msg.set_content(body)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(msg)
def send_verification_email(email:str,token:str):
    verification_link = f"http://localhost:8000/auth/verify_email?token={token}"
    body = f"""
        Hi {email},

        Thank you for signing up.

        Please click the link below to verify your email:

        {verification_link}

        This verification link will expire in 30 minutes.

        If you did not create this account, you can safely ignore this email.

        Regards,
        Insurance Premium Predictor Team
        """

    send_email(email, "Email Verification", body)
def send_password_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"

    body = f"""
Hi {email},

We received a request to reset your password.

Please click the link below to reset your password:

{reset_link}

This password reset link will expire in {settings.RESET_PASSWORD_TOKEN_EXPIRE_MINUTES} minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
Insurance Premium Predictor Team
"""

    send_email(
        email=email,
        subject="Reset Your Password",
        body=body
    )