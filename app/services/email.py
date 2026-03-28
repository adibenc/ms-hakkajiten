"""Email service for sending emails"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from core.config import config
from typing import Optional


class EmailService:
    """Email service for sending emails"""

    def __init__(self):
        self.config = config
        # Template environment for email templates
        try:
            self.template_env = Environment(
                loader=FileSystemLoader(f"{config.APPROOT}{config.TEMPLATES_DIR}/auth/mailables")
            )
        except:
            # Fallback if directory doesn't exist yet
            self.template_env = None

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ):
        """
        Send HTML email

        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            from_email: Sender email (optional, uses config default)
            from_name: Sender name (optional, uses config default)
        """
        if self.config.MAIL_DRIVER == "terminal":
            # Terminal mode - just print
            print(f"\n{'='*60}")
            print(f"EMAIL TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"{'='*60}")
            print(html_content)
            print(f"{'='*60}\n")
            return

        # SMTP mode
        from_addr = from_email or self.config.MAIL_FROM
        from_display = from_name or self.config.MAIL_FROM_NAME

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{from_display} <{from_addr}>"
        message["To"] = to_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        await aiosmtplib.send(
            message,
            hostname=self.config.MAIL_HOST,
            port=self.config.MAIL_PORT,
            username=self.config.MAIL_USERNAME,
            password=self.config.MAIL_PASSWORD,
            start_tls=True
        )

    async def send_password_reset(self, to_email: str, token: str):
        """
        Send password reset email

        Args:
            to_email: Recipient email
            token: Password reset token
        """
        reset_url = f"{self.config.APP_URL}/password/reset?token={token}"

        # Simple HTML template (can be replaced with Jinja2 template)
        html_content = f"""
        <html>
            <head></head>
            <body>
                <h2>Password Reset Request</h2>
                <p>You requested a password reset. Click the link below to reset your password:</p>
                <p><a href="{reset_url}">Reset Password</a></p>
                <p>Or copy this URL: {reset_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you did not request this reset, please ignore this email.</p>
            </body>
        </html>
        """

        # If template environment available, use template
        if self.template_env:
            try:
                template = self.template_env.get_template("reset_password.html")
                html_content = template.render(
                    token=token,
                    reset_url=reset_url,
                    app_url=self.config.APP_URL
                )
            except:
                pass  # Use default template above

        await self.send_email(
            to_email=to_email,
            subject="Reset Your Password",
            html_content=html_content
        )
