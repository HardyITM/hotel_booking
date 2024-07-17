from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.bookings]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    column_export_list = [User.id, User.email]
    
class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user]
    name = 'Бронь'
    name_plural = 'Брони'
    
    icon = 'fa-solid fa-book'
    
    column_export_list = [c.name for c in Booking.__table__.c]
    
class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel, Room.bookings]
    name = 'Комната'
    name_plural = 'Комнаты'
    
    icon = 'fa-solid fa-bed'
    
    column_export_list = [c.name for c in Room.__table__.c]
    
class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.rooms]
    name = 'Отель'
    name_plural = 'Отели'
    
    icon = 'fa-solid fa-hotel'
    
    column_export_list = [c.name for c in Hotel.__table__.c]