from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from database import sessionlocal
from models import Users
from starlette import status
from auth import get_current_user
from passlib.context import CryptContext  # type: ignore


router = APIRouter(prefix="/users", tags=["users"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    return db.query(Users).filter(user["id"] == Users.id).all()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    new_password: str = Query(min_length=5),
):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    user_model = db.query(Users).filter(user["id"] == Users.id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="user is not found")
    user_model.hashed_password = bcrypt_context.hash(new_password)
    db.add(user_model)
    db.commit()


@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    new_phone_number: int = Query(gt=111),
):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    user_model = db.query(Users).filter(user["id"] == Users.id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="user is not found")
    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()
