from pydantic import BaseModel, Field
from typing import Optional,List

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