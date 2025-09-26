from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import create_access_token, verify_password, get_current_user, get_password_hash
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from pydantic import BaseModel
from fastapi import Body

router = APIRouter()

# Tạo user test nếu chưa có trong DB (chỉ chạy khi import file)
def ensure_test_user():
    from app.db.base import SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "testuser").first()
        if not user:
            user = User(username="testuser", hashed_password=get_password_hash("testpass"))
            db.add(user)
            db.commit()
    finally:
        db.close()

ensure_test_user()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(login_data: LoginRequest = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token}


@router.get("/me")
def read_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "username": user.username}
