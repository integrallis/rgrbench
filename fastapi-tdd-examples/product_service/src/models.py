"""Product model - minimal implementation"""

from sqlalchemy import Column, Integer, String

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    version = Column(Integer, default=1)
