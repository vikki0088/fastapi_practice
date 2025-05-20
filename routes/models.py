from routes.databse import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey


class Users(Base):
    __tablename__ = "users"
    Id = Column(Integer,primary_key=True,autoincrement=True)
    Username = Column(String(50),unique=True)
    FirstName = Column(String(100))
    LastName = Column(String(100))
    Email = Column(String(100))
    HashedPassword = Column(String(100))
    IsActive = Column(Boolean)
    user_role = Column(String,nullable=False)


class BookStore(Base):
    __tablename__ = "book_store"
    Id  =  Column(Integer,primary_key=True,autoincrement=True)
    Title = Column(String(50))
    Author = Column(String(50))
    Description = Column(String(200))
    Price = Column(Integer)
    Category = Column(String)
    Is_published = Column(Boolean)
    user_id = Column(Integer,ForeignKey("users.Id"))


# Create tables
Base.metadata.create_all(bind=engine)


