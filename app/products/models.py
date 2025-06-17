from sqlalchemy import Column, Integer, String, Float # SQLAlchemy classes to define table columns and their data types.
from app.core.database import Base

class Product(Base):
    __tablename__ = 'products' #table name as per db 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String)
    image_url = Column(String)
    
