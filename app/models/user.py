from sqlalchemy import Column, BigInteger, String, Boolean, Date
from app.models.model_base import BigIntBaseModel

class User(BigIntBaseModel):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
