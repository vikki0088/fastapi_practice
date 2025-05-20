import secrets
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from routes.databse import db_dependency
from pydantic import BaseModel,Field
from routes.models import Users
from passlib.context import CryptContext
from routes.store import user_dependency


router = APIRouter(
    tags=['users'],
    prefix='/users'
)


# Create a CryptContext instance with bcrypt as default scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = 'HS256'


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordValidation(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class UserValidation(BaseModel):
    UserName: str = Field(min_length=3)
    FirstName: str = Field(min_length=3)
    LastName : str = Field(min_length=3)
    Email: str
    Password: str = Field(min_length=8)
    user_role: str = Field(default=None)
    IsActive: bool = Field(default=False)



@router.post("/create_user",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserValidation, db: db_dependency):
    new_user = Users()
    new_user.Username = user.UserName
    new_user.FirstName = user.FirstName
    new_user.LastName = user.LastName
    new_user.Email = user.Email
    new_user.HashedPassword = hash_password(user.Password)
    new_user.IsActive = True
    new_user.user_role = user.user_role
    db.add(new_user)
    db.commit()


@router.put("/update_password",status_code=status.HTTP_201_CREATED)
async def update_password(db: db_dependency,user: user_dependency,password_request: PasswordValidation):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authorised")

    user = db.query(Users).filter(Users.Id == user.get("user_id")).first()
    if not pwd_context.verify(password_request.password,user.HashedPassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="wrong password..!")
    user.HashedPassword = hash_password(password_request.new_password)
    db.add(user)
    db.commit()


@router.get("/get_user",status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authorised")
    user = db.query(Users).filter(Users.Id == user.get("user_id")).first()
    return user


