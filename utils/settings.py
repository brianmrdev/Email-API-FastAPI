import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.auth_token = os.getenv("AUTHORIZATION_TOKEN")

settings = Settings()
