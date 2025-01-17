from fastapi import status, HTTPException


class BookingException(HTTPException):
    status_code = 500  # задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# Наследуемся от нашего класса
class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Токен истёк'


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Токен отсутствует'


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Невернвый формат токена'


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"

class BookingCannotBeDeleted(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не удалось удалить букинг"