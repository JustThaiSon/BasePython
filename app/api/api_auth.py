from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.schemas.auth_schemas import LoginRequest, RegisterRequest, LoginResponse, UserResponse
from app.schemas.response_code_enum import ResponseCodeEnum, get_message
from app.schemas.sche_base import DataResponse
from app.services.auth_service import AuthService
from fastapi import Body

router = APIRouter()


@router.post("/register", response_model=DataResponse[dict])
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    new_user = auth_service.register_user(register_data)

    return DataResponse[dict](
        code=ResponseCodeEnum.SUCCESS,
        message=get_message(ResponseCodeEnum.SUCCESS),
        data=None  # optional
    )


@router.post("/login", response_model=DataResponse[dict])
def login(login_data: LoginRequest = Body(...), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.authenticate_user(login_data)


@router.get("/me", response_model=UserResponse)
def read_me(user: User = Depends(get_current_user)):
    return user
