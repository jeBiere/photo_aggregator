import smtplib
from email.mime.text import MIMEText
from fastapi import BackgroundTasks
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email_notification(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def schedule_studio_notification(
    background_tasks: BackgroundTasks,
    studio_email: str,
    order_info: dict
):
    subject = "Новый заказ на вашу фотостудию 📸"
    body = (
        f"📅 Дата съёмки: {order_info['shoot_date']}\n"
        f"⏰ Время: {order_info['start_time']}\n"
        f"⏳ Длительность: {order_info['duration']} часов\n"
        f"👤 ID фотографа: {order_info.get('photographer_id') or '-'}\n"
        f"📍 Адрес: {order_info.get('address') or '-'}\n"
        f"📝 Комментарий: {order_info.get('special_requests') or 'отсутствует'}\n"
    )
    background_tasks.add_task(send_email_notification, studio_email, subject, body)
