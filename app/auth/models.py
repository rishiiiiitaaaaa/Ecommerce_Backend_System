from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.core.logger import logger 

# SQLAlchemy model representing the 'users' table in the database.
class User(Base):
    __tablename__ = "users"  # Table name in the database

    # Columns in the 'users' table
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True)
   
