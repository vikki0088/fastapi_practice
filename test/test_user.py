from test.utils import *
from routes.databse import get_db
from routes.auth import get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_get_user(test_user):
    response = client.get("/users/get_user")
    assert response.status_code == 200



def test_password_change(test_user):
    response = client.put("/users/update_password",json={
        'password': "12345678901",
        'new_password': "chikki@123"
    })

    assert response.status_code == status.HTTP_201_CREATED


