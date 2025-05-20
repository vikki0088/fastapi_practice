from test.utils import *
from routes.auth import get_current_user,authenticate_user,create_access_token,SECRET_KEY,ALGORITHM
from routes.databse import get_db
from datetime import timedelta
from jose import jwt
import pytest


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_user(test_user):
    db =TestingSessionLocal()
    authenticated_user = authenticate_user(username=test_user.Username,password='12345678901',db=db)
    assert authenticated_user is not None
    assert authenticated_user.Username == test_user.Username


    non_existing_user = authenticate_user("wrong_username",password='12345678901',db=db)
    assert non_existing_user is False

    wrong_password_user = authenticate_user(username=test_user.Username,password='wrong_password',db=db)
    assert wrong_password_user is False



def test_create_access_token(test_user):
    token = create_access_token(username=test_user.Username,user_id=test_user.Id,role=test_user.user_role,expires_delta=timedelta(20))
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],
                               options={'verify_signature': False})
    assert decoded_token['username'] == test_user.Username
    assert decoded_token['user_id'] == test_user.Id
    assert decoded_token['user_role'] == test_user.user_role


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {
        'username': "test_user",
        'user_id': 1,
        "user_role": "admin"
    }
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user == {
        'username': "test_user",
        'user_id': 1,
        "user_role": "admin"
    }