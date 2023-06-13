import uuid
from typing import Literal, Optional,List
from pydantic import BaseModel, Field


# va a estar embebido en movies
class Review(BaseModel):
    text: str = Field(...)
    score: int = Field(ge=1, le=5)
    #user: uuid.UUID # el _id del usuario; lo validaremos a nivel de la app
    user: str = Field(...)


class Movie(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    genres: Optional[List[Literal['action', 'drama','comedy']]]


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Mad Max",
                "genres":['action','comedy'],
            }
        }


        
class MovieUpdate(BaseModel):
    title: str = Field(...)
    genres: Optional[List[Literal['action', 'drama','comedy']]]

    class Config:
        schema_extra = {
            "example": {
                "title": "Mad Max the road warrior",
                "genres":['action','drama'],
            }
        }


class MovieOut(Movie):
    reviews: Optional[List[Review]] = []