from test.utils import *
from routes.databse import get_db
from routes.auth import get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated_admin(test_book_store):
    response = client.get("/admin/get_all_books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'Author': 'vikki',
                                'Category': 'love',
                                'Description': 'learn about love and war',
                                'Id': 1,
                                'Price' : 200,
                                'Title': 'love and war',
                                'Is_published': True,
                                'user_id': 1}]


def test_delete_book_authenticated_admin(test_book_store):
    response = client.delete("/admin/delete_book/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(BookStore).filter(BookStore.Id == 1).first()
    assert model is None

def test_admin_book_not_found():
    response = client.delete("/admin/delete_book/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "book not found"}
