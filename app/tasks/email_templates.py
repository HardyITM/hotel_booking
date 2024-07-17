from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings as s


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr
    ):
    email = EmailMessage()
    
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = s.SMTP_USER
    email['To'] = email_to
    
    email.set_content(
        f"""
            Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        """,
        subtype='html'
    )
    
    return email