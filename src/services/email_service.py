from fastapi_mail import FastMail, MessageSchema
from src.core.email_config import conf

class   EmailService:
    @staticmethod
    async def send_tag_approved_email(to_email: str, tag_name: str):
        message = MessageSchema(
            subject="Your Tag Was Approved 🎉",
            recipients=[to_email],
            body=f"Great news! Your tag '{tag_name}' has been approved.",
            subtype="plain"
        )

        fm = FastMail(conf)
        await fm.send_message(message)
