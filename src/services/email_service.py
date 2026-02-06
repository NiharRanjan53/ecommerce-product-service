from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.core.email_config import conf

class EmailService:
    # Initialize FastMail once to reuse the connection
    fm = FastMail(conf)

    @staticmethod
    async def send_tag_approved_email(to_email: str, tag_name: str):
        message = MessageSchema(
            subject="Your Tag Was Approved 🎉",
            recipients=[to_email],
            body=f"Great news! Your tag '{tag_name}' has been approved.",
            subtype="plain"
        )
        await EmailService.fm.send_message(message)

    @staticmethod
    async def send_profile_update_email(to_email: str, username: str = "User"):
        html_content = EmailService.get_profile_update_template(username)
        
        message = MessageSchema(
            subject="Security Notification: Profile Updated",
            recipients=[to_email],
            body=html_content,
            subtype="html"
        )
        await EmailService.fm.send_message(message)

    @staticmethod
    def get_profile_update_template(username: str):
        # In a real project, load this from a .html file!
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="padding: 20px;">
                    <h2>Profile Updated</h2>
                    <p>Hello {username}, your profile was updated.</p>
                </div>
            </body>
        </html>
        """