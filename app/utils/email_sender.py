import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your sender email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password (e.g. Gmail app password)

def send_email(subject: str, recipient: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
