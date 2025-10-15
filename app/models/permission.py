from sqlalchemy import Column, String
from app.models.model_base import BigIntBaseModel

class Permission(BigIntBaseModel):
    __tablename__ = 'permissions'

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
