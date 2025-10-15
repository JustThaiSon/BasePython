from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth_schemas import RegisterRequest, LoginRequest, LoginResponse, UserResponse
from app.schemas.sche_base import ResponseSchemaBase
from app.schemas.response_code_enum import ResponseCodeEnum
from typing import Optional, Dict, Any

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, register_data: RegisterRequest) -> User:
        """Đăng ký user mới"""
        # Kiểm tra username đã tồn tại
        existing_user = self.db.query(User).filter(User.username == register_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Kiểm tra email đã tồn tại
        existing_email = self.db.query(User).filter(User.email == register_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Tạo user mới
        new_user = User(
            username=register_data.username,
            email=register_data.email,
            hashed_password=get_password_hash(register_data.password),
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            phone_number=register_data.phone_number,
            address=register_data.address,
            gender=register_data.gender,
            date_of_birth=register_data.date_of_birth,
            is_active=True
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def authenticate_user(self, login_data: LoginRequest) -> Dict[str, Any]:
        """Xác thực và đăng nhập user"""
        try:
            # Tìm user theo username hoặc email
            user = self.db.query(User).filter(
                (User.username == login_data.username) | (User.email == login_data.username)
            ).first()

            if not user or not verify_password(login_data.password, user.hashed_password):
                return ResponseSchemaBase.custom_response(
                    ResponseCodeEnum.UNAUTHORIZED,
                    data=None,
                )

            if not user.is_active:
                return ResponseSchemaBase.custom_response(
                    ResponseCodeEnum.UNAUTHORIZED,
                    data=None,
                )

            access_token = create_access_token(user_id=user.id)
            login_response = LoginResponse(access_token=access_token)

            return ResponseSchemaBase.success_response(
                data=login_response.model_dump(),
            )

        except Exception as e:
            return ResponseSchemaBase.custom_response(
                ResponseCodeEnum.SYSTEM_ERROR,
                data=None,
            )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Lấy user theo ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Lấy user theo username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Lấy user theo email"""
        return self.db.query(User).filter(User.email == email).first()

    def update_user_status(self, user_id: int, is_active: bool) -> User:
        """Cập nhật trạng thái hoạt động của user"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)

        return user
