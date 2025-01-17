from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pydantic import EmailStr
from app.config import settings
import app.exceptions as excep
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.HASH_METHOD
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise excep.TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.HASH_METHOD
        )
    except JWTError:
        raise excep.IncorrectTokenFormatException
    expire: str = payload.get("exp")
    now = datetime.now(timezone.utc).timestamp()
    if not expire or (int(expire) < int(now)):
        raise excep.TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise excep.UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise excep.UserIsNotPresentException
    return user
