from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="User already registered"


class InvalidEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Invalid login or password'


class MissingTokenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Missing JWT token'


class InvalidTokenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Invalid JWT token'


class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Expired JWT token'


class UserNotFoundException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCanNotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail='Impossible to book'
    
class BookingNotFound(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail='Booking not found'