from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from typing import Annotated
from sqlalchemy.orm import session
from fastapi import Depends

# SQLAlchemy database URL
DATABASE_URL = f"mysql+pymysql://root:Vishnu12345@localhost:3306/book_store"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)
# Create a base class for ORM models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()  # Create a new DB session
    try:
        yield db          # Provide it to the request
    finally:
        db.close()        # Ensure it's closed after the request is done


db_dependency = Annotated[session, Depends(get_db)]