from sqlalchemy import Column, BigInteger
from app.models.model_base import Base

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(BigInteger, nullable=False, primary_key=True)
    permission_id = Column(BigInteger, nullable=False, primary_key=True)
