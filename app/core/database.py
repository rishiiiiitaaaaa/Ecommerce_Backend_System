from sqlalchemy import create_engine #This function is used to set up the connection to the database
from sqlalchemy.ext.declarative import declarative_base #a factory function that returns a base class for declarative class definitions 
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/ecommerce_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL) #engine is used by SQLAlchemy to communicate with the PostgreSQL database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
