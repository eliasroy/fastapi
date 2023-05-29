from fastapi import APIRouter
from fastapi import Path,Query,Depends
from fastapi.responses import JSONResponse#importaciòn de la clase para utilizar html
from typing import List

from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from service.movie import MovieService
from schema.movie import Movie
movie_router=APIRouter()


#creaciòn de la ruta peliculas, y la etiqueta peliculas
@movie_router.get('/movies', tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies()->List[Movie]: #devuelve el listado de las peliculas
    db=Session()
    result=MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#con parametro
@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int=Path(ge=1,le=2000))->Movie:
    db=Session
    result=MovieService(db).get_movie(id)
    if not result:
       return  JSONResponse(status_code=404,content={"message":"no se encontro"})
    return  JSONResponse(status_code=200,content=jsonable_encoder(result)) 

#parametro query
@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_cat(category:str=Query(min_length=5,max_length=15))->List[Movie]:
    db=Session()
    cat=MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200,content=jsonable_encoder(cat))

@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movies(movie:Movie)->dict:
    db=Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})


@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict)
def update_movies(id:int ,movie:Movie)->dict:
    db=Session()
    MovieService(db).update_movie(id,mo)
    return JSONResponse(status_code=404,content={"message":"Se ha actualizado la pelicula"})

@movie_router.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movies(id:int )->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "no se ha encontrado la pelicula"}, status_code=404)

    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "se ha eliminado la pelicula"}, status_code=200)

