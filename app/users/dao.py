from app.dao.base import BaseDAO

from .models import User


class UsersDAO(BaseDAO):
    model = User