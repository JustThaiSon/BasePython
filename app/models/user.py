from sqlalchemy import Column, Integer, String
from app.models.model_base import BareBaseModel

class User(BareBaseModel):
    __tablename__ = 'users'
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

