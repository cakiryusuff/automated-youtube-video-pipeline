import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.logger import get_logger
from utils.common_functions import load_config

class EmailSender:
    def __init__(self, use_tls: bool = True):
        self.logger = get_logger(__name__)
        self.config = load_config("config/config.yaml")
        self.smtp_server = self.config["smtp_server"]["host"]
        self.port = self.config["smtp_server"]["port"]
        self.sender_email = self.config["smtp_server"]["sender"]
        self.password = self.config["smtp_server"]["password"]
        self.use_tls = use_tls

    def send_email(self, recipient_email, subject, body, is_html=False):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        if is_html:
            message.attach(MIMEText(body, 'html'))
        else:
            message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            if self.use_tls:
                server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(message)
            server.quit()
            print("E-mail sent successfully.")
            self.logger.info("E-mail sent successfully.")
        except Exception as e:
            print("Error sending e-mail:", e)
            self.logger.error(f"Error sending e-mail: {e}")
            raise e

if __name__ == "__main__":
    config = load_config("config/config.yaml")
    subject = "Test E-postası"
    body = "Bu bir test e-postasıdır."
    to = "ckryusuff@gmail.com"

    email_sender = EmailSender()
    email_sender.send_email(to, subject, body)
