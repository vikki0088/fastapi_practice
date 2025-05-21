from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from routes.databse import db_dependency
from routes.models import Users
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt,JWTError
import secrets

router = APIRouter(
    tags=['Auth'],
    prefix='/auth'
)

templates = Jinja2Templates(directory='./templates')
router.mount("/static",StaticFiles(directory="static"),name="static")


# Create a CryptContext instance with bcrypt as default scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oath2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
SECRET_KEY = secrets.token_urlsafe(64)
ALGORITHM = 'HS256'


#### pages #####

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html",{'request': request})


@router.get("/register-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("register.html",{'request': request})



######end points ##########
def create_access_token(username: str,user_id: int,role:str,expires_delta: timedelta):
    encode = {
        "username": username,
        "user_id": user_id,
        "user_role": role
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def authenticate_user(username: str, password: str,db):
    user = db.query(Users).filter(Users.Username == username).first()
    if not user: return False
    if not pwd_context.verify(password,user.HashedPassword): return False
    return user

@router.post("/token")
async def login_for_access_token(db: db_dependency,form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    token = create_access_token(username=user.Username,user_id=user.Id,role = user.user_role,expires_delta=timedelta(20))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

async def get_current_user(token: str = Depends(oath2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('username')
        user_id: str = payload.get('user_id')
        user_role:str = payload.get('user_role')
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="UnAuthorised")
        return {
            "username": username,
            "user_id": user_id,
            "user_role": user_role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="UnAuthorised")