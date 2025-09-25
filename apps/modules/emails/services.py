import os, aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .config import *
from .exception import ErrorCode

class EmailService:
    def __init__(self):
        template_dir = os.path.join("assets", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))


    async def _send_mail(self, message: MIMEMultipart):
        try:
            client = aiosmtplib.SMTP(
                hostname=HOST_SMTP,
                port=PORT_SMTP,
                username=USERNAME_SMTP,
                password=PASSWORD_SMTP,
                start_tls=True,
            )
            await client.connect()
            await client.send_message(message)
            await client.quit()
        except Exception:
            raise ErrorCode.SendMailFailed()


    async def send_otp_email(self, email: str, fullname: str, data: str):
        try:
            template = self.env.get_template("email_otp.html")
            html_content = template.render(fullname=fullname, otp_code=data)

            message = MIMEMultipart("alternative")
            message["From"] = USERNAME_SMTP
            message["To"] = email
            message["Subject"] = "[MAKEUP] Verification Code"
            message.attach(MIMEText(html_content, "html", "utf-8"))

            print(f"[Service] OTP email sent successfully to {email}")
            await self._send_mail(message)

        except Exception:
            raise ErrorCode.SendMailFailed()


    async def send_invoice_email(self, email: str, fullname: str, data: dict):
        try:
            data = data.copy()
            data["fullname"] = fullname

            template = self.env.get_template("email_invoice.html")
            html_content = template.render(**data)

            message = MIMEMultipart("alternative")
            message["From"] = USERNAME_SMTP
            message["To"] = email
            message["Subject"] = "[MAKEUP] Infomation Invoice"
            message.attach(MIMEText(html_content, "html", "utf-8"))

            print(f"[Service] Invoice email sent successfully to {email}")
            await self._send_mail(message)

        except Exception:
            raise ErrorCode.SendMailFailed()
