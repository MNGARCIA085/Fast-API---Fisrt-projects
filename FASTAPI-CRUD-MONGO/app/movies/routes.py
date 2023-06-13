
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from .models import Movie,MovieUpdate,Review,MovieOut



router = APIRouter(
    prefix="/movies",
    responses={404: {"description": "Not found"}},
    tags=['movies'],
)

@router.post("/", response_description="Create a new book", 
                status_code=status.HTTP_201_CREATED,
                response_model=MovieOut)
def create_movie(request: Request, movie: Movie = Body(...)):
    # si la peli ya fue ingresada retorno
    if (request.app.database["movies"].find_one({"title": movie.title})) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie already added")
    # en otro caso inserto el registro
    movie = jsonable_encoder(movie)
    new_movie = request.app.database["movies"].insert_one(movie)
    created_movie = request.app.database["movies"].find_one(
        {"_id": new_movie.inserted_id}
    )
    return created_movie




@router.get("/", response_description="List all movies", response_model=List[MovieOut])
def list_movies(request: Request):
    return list(request.app.database['movies'].find(limit=100))



@router.get("/{id}", response_description="Get a single book by id", response_model=MovieOut)
def find_movie(id: str, request: Request):
    if (movie := request.app.database["movies"].find_one({"_id": id})) is not None:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")




@router.put("/{id}", status_code=status.HTTP_201_CREATED,response_description="Update a movie", response_model=Movie)
def update_movie(id: str, request: Request, movie: MovieUpdate = Body(...)):
    movie = {k: v for k, v in movie.dict().items() if v is not None}

    if len(movie) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"_id": id}, {"$set": movie}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

    if (
        existing_movie := request.app.database["movies"].find_one({"_id": id})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")



@router.delete("/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.database["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")



"""

REVIEWS, we need to add it to a movie; see the reviews for a movie....

"""


@router.post("/{id}/reviews/", response_description="Add a review to a movie")
def add_review(id: str, request: Request, review: Review = Body(...)):

    # que el usuario exista
    if (request.app.database["users"].find_one({"_id": review.user})) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The user does not exist")

    # que el usuario pueda ingresar una única review
    if (request.app.database["movies"].find_one({"_id": id,"reviews.user":review.user})) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user already reviewed this movie")

    review = jsonable_encoder(review)
    request.app.database["movies"].update_one(
            {"_id": id}, {"$push": {'reviews':review}}
        )

    updated_movie = request.app.database["movies"].find_one(
        {"_id": id}
    )
    return updated_movie





# datos de las películas
# promedio de puntajes de todas las películas
@router.get("/scores/", response_description="Average score of the movies")
def add_review(request: Request): # maybe an id filter later

    averages = request.app.database['movies'].aggregate([
            {
                "$unwind":"$reviews"
            },
            {
                "$group": {
                    "_id": {
                        "_id": "$_id",
                        "title": "$title"
                        },
                    "reviews":{
                        "$push": "$reviews.score"
                    },
                    "reviews_average": {
                        "$avg": "$reviews.score",
                    },
                    "reviews_count": {
                        "$count": {}
                    }
                }
            },
            {
                "$project":{
                    "_id": 0,
                    "title": "$_id.title",
                    "reviews_average": 1,
                    "reviews_count":1,
                    "reviews": 1
                }
            }
    ])

    lista = []
    for a in averages:
        lista.append({'title':a['title'],'score':a['reviews_average'],'count':a['reviews_count']})

    return lista



