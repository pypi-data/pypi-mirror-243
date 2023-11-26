import smtplib
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from typing import List, Literal


class SimpleMailSender:
    def __init__(
        self,
        host: str,
        port: int,
        protocol: Literal["SSL", "TLS"],
        user: str,
        password: str,
    ) -> None:
        self.host = host
        self.port = port
        self.protocol = protocol
        self.user = user
        self.password = password

    def send(
        self,
        sender: str,
        targets: List[str],
        subject: str,
        body: str,
        attachment_path: str,
    ) -> None:
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(targets)
        message.attach(MIMEText(body))

        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_path.split('/')[-1]}",
        )

        message.attach(part)

        if self.protocol == "TLS":
            server = smtplib.SMTP(self.host, self.port)
            context = ssl.create_default_context()
            server.starttls()
        elif self.protocol == "SSL":
            server = smtplib.SMTP_SSL(self.host, self.port)

        server.login(self.user, self.password)
        server.sendmail(sender, targets, message.as_string())
        server.quit()
