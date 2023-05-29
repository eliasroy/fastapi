from fastapi import FastAPI,Body,Path,Query,HTTPException,Depends
from fastapi.responses import HTMLResponse,JSONResponse#importaciòn de la clase para utilizar html
from pydantic import BaseModel, Field
from typing import Optional,List
from routers.movie import movie_router
from routers.login import login_router
from starlette.requests import Request
from utils.jwt_manager   import create_token,validacion
from fastapi.security import HTTPBearer
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from middlewares.error_handler import ErrorHandler
import uvicorn
import os
app = FastAPI() 
app.title = "My aplicación con FastAPI" 
app.version = "0.0.1" 
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)))
