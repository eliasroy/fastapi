from fastapi import FastAPI,Body,Path,Query,HTTPException,Depends
from fastapi.responses import HTMLResponse,JSONResponse#importaciòn de la clase para utilizar html
from pydantic import BaseModel, Field
from typing import Optional,List

from starlette.requests import Request
from jwt_manager   import create_token,validacion
from fastapi.security import HTTPBearer


app = FastAPI() 
app.title = "My aplicación con FastAPI" 
app.version = "0.0.1" 

class JWTBearer(HTTPBearer):
  async  def __call__(self, requests: Request) :
        auth= await super().__call__(requests)
        data=validacion(auth.credentials)
        if data['email']!='admin@gmail.com':
            raise HTTPException(status_code=403,detail="Credenciales invalidas")


class User(BaseModel):
    email:str
    password:str


class Movie(BaseModel):
    id:Optional[int]=None
    title:str =Field(max_length=15,min_length=5,)
    overview:str=Field(max_length=50,min_length=5)
    year:int=Field(le= 2022)
    rating:float 
    category:str=Field(max_length=15,min_length=5,)
    class Config:
        schema_extra={
            "example":{
                "id":0,
                "title":"mipelicula",
                "overview":"desccription of movie",
                "year":2022,
                "rating":1,
                "category":"accion"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Aventura'    
    } ,
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]
#creacion del endpoin
@app.get('/', tags=['home']) 
def message():
    return HTMLResponse('<h1>Hello world</h1>') #utilizando html

#creaciòn de la ruta peliculas, y la etiqueta peliculas
@app.get('/movies', tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies()->List[Movie]: #devuelve el listado de las peliculas
    return JSONResponse(status_code=200, content=movies)

#con parametro
@app.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int=Path(ge=1,le=2000))->Movie:
    movie = list(filter(lambda x: x['id'] == id,movies))
    return  JSONResponse(content=movie) if len(movie) > 0 else"No hay nada que ver"

#parametro query
@app.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_cat(category:str=Query(min_length=5,max_length=15))->List[Movie]:
     movie = list(filter(lambda x: x['category'] == category ))
     return JSONResponse(content=movie) if len(movie) > 0 else"No hay nada que ver"

@app.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movies(movie:Movie)->dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})


@app.put('/movies/{id}',tags=['movies'],response_model=dict)
def update_movies(id:int ,movie:Movie)->dict:
    for item in movies:
       if  item['id']==movie.id:
           item['title']=movie.title
           item['overview']=movie.overview
           item['year']=movie.year
           item['rating']=movie.rating
           item['category']=movie.category
    return JSONResponse(status_code=404,content={"message":"Se ha actualizado la pelicula"})

@app.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movies(id:int )->dict:
    for item in movies:
       if  item['id']==id:
           movies.remove(item)
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})


@app.post("/login",tags=['auth'])
def login(user:User):
    if user.email=="admin@gmail.com" and user.password=="admin":
        toke:str=create_token(user.dict())
        return JSONResponse(status_code=200,content=toke)