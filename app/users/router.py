from fastapi import APIRouter, Depends, Response
from fastapi_versioning import version

from app.exceptions import (InvalidEmailOrPasswordException,
                            UserAlreadyExistsException)

from .auth import (authenticate_user, create_access_token, get_password_hash,
                   verify_password)
from .dao import UsersDAO
from .dependencies import get_current_user
from .models import User
from .schemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags=["Auth * Users"]
)

@router.post("/register")
@version(1)
async def register_user(user_data: SUserAuth):
    email = user_data.email
    existing_user = await UsersDAO.find_one_or_none(email=email)
    if existing_user:
        raise UserAlreadyExistsException
    
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_data(email=email, hashed_password=hashed_password)
    return {"Info": "Complete"}

@router.post("/login")
@version(1)
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        'booking_access_token',
        access_token,
        httponly=True,
        secure=True
    )
    return access_token

@router.post('/logout')
@version(1)
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')
    return 

@router.get('/me')
@version(1)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user