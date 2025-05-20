from routes.databse import get_db
from routes.auth import get_current_user
from fastapi import status
from test.utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_read_all_authenticated(test_book_store):
    response = client.get("/store/get_all_books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'Author': 'vikki',
                                'Category': 'love',
                                'Description': 'learn about love and war',
                                'Id': 1,
                                'Price' : 200,
                                'Title': 'love and war',
                                'Is_published': True,
                                'user_id': 1}]



def test_read_one_authenticated(test_book_store):
    response = client.get("/store/get_book/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'Author': 'vikki',
                                'Category': 'love',
                                'Description': 'learn about love and war',
                                'Id': 1,
                                'Price' : 200,
                                'Title': 'love and war',
                                'Is_published': True,
                                'user_id': 1}

def test_read_one_authenticated_not_fount():
    response = client.get("/store/get_book/139434")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "book not found..!"}


def test_add_book(test_book_store):
    request_book = {'Author': 'keerthana',
                    'Category': 'sports',
                    'Description': 'learn about cricket',
                    'Price' : 250,
                    'Title': 'cricket is love',
                    'Is_published': True,
                    'user_id': 1}

    response = client.post("/store/create_book",json=request_book)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(BookStore).filter(BookStore.Id == 2).first()
    assert model.Title == request_book.get('Title')
    assert model.Category == request_book.get('Category')



def test_delete_book(test_book_store):
    response = client.delete("/store/delete_book/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(BookStore).filter(BookStore.Id == 1).first()
    assert model is None


def test_delete_book_not_found():
    response = client.delete("/store/delete_book/12345")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "book not found"}



