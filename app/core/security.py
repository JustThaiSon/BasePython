from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt as jose_jwt
from sqlalchemy.orm import Session

from typing import Any, Union
from app.core.config import settings
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.db.base import get_db
from app.models.user import User
from app.schemas.sche_base import DataResponse
from app.schemas.response_code_enum import ResponseCodeEnum, get_message

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: Union[int, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    to_encode = {
        "exp": expire, "user_id": str(user_id)
    }
    encoded_jwt = jose_jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jose_jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_token_from_header(request: Request) -> str:
    auth_header = request.headers.get("authorization")
    if not auth_header:
        # Raise HTTPException instead of returning JSONResponse
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return auth_header.strip()


def get_current_user(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # Bcrypt chỉ hỗ trợ tối đa 72 ký tự, cắt password nếu dài hơn
    password = password[:72]
    return pwd_context.hash(password)
