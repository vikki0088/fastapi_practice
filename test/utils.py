from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,text
from fastapi.testclient import TestClient
from routes.models import Base
from sqlalchemy.pool import StaticPool
from main import app
import pytest
from routes.models import BookStore,Users
from routes.users import hash_password


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       echo_pool=True)



TestingSessionLocal = sessionmaker(autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        'username': "keerthana01",
        'user_id': 1,
        'user_role': 'admin'
    }

client =TestClient(app)


@pytest.fixture
def test_book_store():
    new_book = BookStore(
        Title = "love and war",
        Author = "vikki",
        Description = "learn about love and war",
        Price = 200,
        Category = "love",
        Is_published = True,
        user_id = 1
    )
    db = TestingSessionLocal()
    db.add(new_book)
    db.commit()
    yield new_book
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM book_store;"))
        connection.commit()



@pytest.fixture
def test_user():
    new_user = Users(
        Username = "keerthana03",
        FirstName = "keerthana",
        LastName = "polati",
        Email = "chikki@email.com",
        HashedPassword = hash_password("12345678901"),
        IsActive = True,
        user_role = 'admin'
    )
    db = TestingSessionLocal()
    db.add(new_user)
    db.commit()
    yield new_user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
