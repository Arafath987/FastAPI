from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import sessionlocal
from ..models import Todos
from starlette import status
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/todos", tags=["todos"])
templates = Jinja2Templates(directory="TodoApp/Templates")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=16)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "title new",
                "description": "description new",
                "priority": 5,
                "complete": True,
            }
        }
    }


class TodoById(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=10)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "title new",
                "description": "description new",
                "priority": 5,
                "complete": True,
            }
        }
    }


###### Pages ######
def redirect_to_login():
    redirect_responce = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_responce.delete_cookie(key="access_token")
    return redirect_responce


@router.get("/todo-page")
async def render_todo_page(db: db_dependency, request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if not user:
            return redirect_to_login()
        todos = db.query(Todos).filter(user["id"] == Todos.owner_id).all()
        return templates.TemplateResponse(
            "todo.html", {"request": request, "todos": todos, "user": user}
        )
    except:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if not user:
            return redirect_to_login()

        return templates.TemplateResponse(
            "add-todo.html", {"request": request, "user": user}
        )

    except:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def edit_todo(db: db_dependency, request: Request, todo_id):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if not user:
            redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse(
            "edit-todo.html", {"request": request, "user": user, "todo": todo}
        )
    except:
        return redirect_to_login()


###### Endpoints #####
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="authemtication failed")

    return db.query(Todos).filter(user["id"] == Todos.owner_id).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user["id"], Todos.id == todo_id)
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todos(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user["id"], todo_id == Todos.id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="the todo is none")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user["id"], todo_id == Todos.id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="id is not found")
    db.delete(todo_model)
    db.commit()


# @router.post("/post_element_by_id", status_code=status.HTTP_201_CREATED)
# async def create_element_by_id(
#     user: user_dependency, db: db_dependency, todo_by_id: TodoById
# ):
#     if user is None:
#         raise HTTPException(status_code=401, detail="authentication failed")
#     todo_model = Todos(**todo_by_id.model_dump(), owner_id=user["id"])
#     db.add(todo_model)
#     db.commit()


# @router.delete("/clear/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail="authentication failed")
#     db.query(Todos).filter(Todos.owner_id == user["id"]).delete()
#     db.commit()
