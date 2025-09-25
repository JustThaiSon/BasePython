from sqlalchemy import Column, Integer, String, Float
from app.models.model_base import Base

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

