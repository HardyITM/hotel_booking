import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings as s
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(
    path:str,
    ):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000, 500))
    im_resized_small = im.resize((200, 100))
    im_resized.save(f"app/static/images/resized_normal_{im_path.name}")
    im_resized_small.save(f"app/static/images/resized_small_{im_path.name}")
    
@celery.task
def send_booking_confirmation(
    booking: dict,
    email_to: EmailStr
    ):
    email_to = s.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to)
    
    with smtplib.SMTP_SSL(s.SMTP_HOST, s.SMTP_PORT) as server:
        server.login(s.SMTP_USER, s.SMTP_PASS)
        server.send_message(msg_content)