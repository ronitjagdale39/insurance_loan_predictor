from passlib.context import CryptContext
from fastapi import Depends
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hashed_password(plain_password:str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {"exp": expire,
        "type":"access_token"}
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
def create_refresh_token(data:dict):
    payload=data.copy()
    expire=datetime.utcnow()+timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    payload.update({
        "exp":expire,
        "type":"refresh_token"
    })
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )