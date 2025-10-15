from sqlalchemy import Column, String
from app.models.model_base import BigIntBaseModel

class Role(BigIntBaseModel):
    __tablename__ = 'roles'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
