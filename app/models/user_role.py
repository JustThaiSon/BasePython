from sqlalchemy import Column, BigInteger, DateTime
from app.models.model_base import Base
from datetime import datetime

class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(BigInteger, nullable=False, primary_key=True)
    role_id = Column(BigInteger, nullable=False, primary_key=True)
    assigned_at = Column(DateTime, default=datetime.now, nullable=False)
