from fastapi import APIRouter,HTTPException,status,Depends
from routes.models import BookStore
from pydantic import Field,BaseModel
from routes.databse import db_dependency
from routes.auth import get_current_user
from typing import Annotated

router = APIRouter(
    tags=['store'],
    prefix='/store'
)


class BookValidation(BaseModel):
    Title: str = Field(min_length=1)
    Author: str = Field(min_length=1)
    Description: str = Field(max_length=200,default=None)
    Category: str = Field(min_length=1)
    Price: int = Field(gt=0)
    Is_published: bool = Field(default=False)

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/get_all_books",status_code=status.HTTP_200_OK)
async def get_all_book(db: db_dependency,user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not permitted to this action!!")
    return db.query(BookStore).filter(BookStore.user_id == user.get("user_id")).all()


@router.get("/get_book/{book_id}",status_code=status.HTTP_200_OK)
async def get_all_book(book_id: int,db: db_dependency,user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not permitted to this action!!")
    book = db.query(BookStore).filter(BookStore.Id == book_id).filter(BookStore.user_id == user.get("user_id")).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="book not found..!")
    return book


@router.post("/create_book",status_code=status.HTTP_201_CREATED)
async def add_new_book(book: BookValidation,db: db_dependency,user: user_dependency):
    new_book = BookStore(**book.model_dump(),user_id=user.get("user_id"))
    db.add(new_book)
    db.commit()


@router.delete("/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int,db: db_dependency,user: user_dependency):
    book = db.query(BookStore).filter(BookStore.Id == book_id).filter(BookStore.user_id == user.get("user_id")).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="book not found")
    db.delete(book)
    db.commit()



