from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from utils.jwt_manager import create_token
from schema.user import User

login_router = APIRouter()


@login_router.get("/", tags=['home'])
def massege():
    return HTMLResponse('<h1>Hello World!</h1>')


@login_router.post("/login", tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)