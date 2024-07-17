from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings as s
from app.exceptions import (InvalidTokenException, MissingTokenException,
                            TokenExpiredException, UserNotFoundException)
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise MissingTokenException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, s.SECRET_KEY, s.ALGORITHM
        )
    except JWTError:
        raise InvalidTokenException
    
    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    
    user_id = payload.get('sub')
    if not user_id:
        raise UserNotFoundException
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
        
    return user