from fastapi import APIRouter,HTTPException,status,Depends
from routes.models import BookStore
from routes.databse import db_dependency
from routes.auth import get_current_user
from typing import Annotated
from routes.models import Users
from pydantic import BaseModel
from typing import List

router = APIRouter(
    tags=['admin'],
    prefix='/admin'
)

user_dependency = Annotated[dict,Depends(get_current_user)]

class UserOut(BaseModel):
    Username: str

    class Config:
        orm_mode = True



@router.get("/read_all_users",status_code=status.HTTP_200_OK,response_model=List[UserOut])
async def read_all_users(db: db_dependency,user: user_dependency):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="action is not permitted..!")

    return db.query(Users).all()


@router.get("/get_all_books",status_code=status.HTTP_200_OK)
async def read_all_books(db: db_dependency,user: user_dependency):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="action is not permitted..!")
    return db.query(BookStore).all()


@router.delete("/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int,db: db_dependency,user: user_dependency):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="action is not permitted..!")
    book = db.query(BookStore).filter(BookStore.Id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="book not found")
    db.delete(book)
    db.commit()
