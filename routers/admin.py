from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import Field
from sqlalchemy.orm import Session
from database import sessionlocal
from models import Todos
from starlette import status
from auth import get_current_user


router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_admin(user: user_dependency, db: db_dependency):
    if user is None or user["user_role"] != "admin":
        raise HTTPException(status_code=401, detail="authentication failed")
    return db.query(Todos).all()
